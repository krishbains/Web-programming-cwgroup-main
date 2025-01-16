from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from rest_framework import viewsets, permissions
from .forms import CustomUserCreationForm
from rest_framework.decorators import action
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Hobby, FriendRequest
from .serializers import HobbySerializer, UserProfileSerializer, FriendRequestSerializer
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import update_session_auth_hash
from django.db import models



def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            api = form.save()
            login(request, api)
            return redirect('/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'api/spa/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect to root URL where Vue SPA is served
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'api/spa/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


class HobbyViewSet(viewsets.ModelViewSet):
    queryset = Hobby.objects.all()
    serializer_class = HobbySerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    @transaction.atomic
    def add_to_profile(self, request):
        name = request.data.get('name', '').lower().strip()

        if not name:
            return Response(
                {'error': 'Name is required'},
                status=status.HTTP_400_BAD_REQUEST
            )


        hobby, created = Hobby.objects.get_or_create(
            name=name,
            defaults={'name': name}
        )

        request.user.hobbies.add(hobby)

        # Use serializer only once for response
        data = {
            'id': hobby.id,
            'name': hobby.name,
            'created': created
        }

        return Response(
            data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )

@method_decorator(ensure_csrf_cookie, name='dispatch')
class UserProfileViewSet(viewsets.GenericViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Return the current authenticated user
        return self.request.user

    @action(detail=False, methods=['get'])
    def me(self, request):
        # Get current user's profile
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        user = self.get_object()
        is_partial = request.method == 'PATCH'

        # Remove empty fields from request data
        cleaned_data = {k: v for k, v in request.data.items() if v is not None and v != ''}

        serializer = self.get_serializer(
            user,
            data=cleaned_data,
            partial=is_partial
        )

        if serializer.is_valid():
            # Check if only password is being updated
            is_password_only_update = set(cleaned_data.keys()).issubset({'current_password', 'new_password'})

            user = serializer.save()

            # If password was changed, update session
            if 'new_password' in serializer.validated_data:
                update_session_auth_hash(request, user)

            return Response(self.get_serializer(user).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required(login_url='login')
def main_spa(request: HttpRequest) -> HttpResponse:
    """
    Main view that serves the Vue SPA.
    If user is not authenticated, they will be redirected to login.
    """
    return render(request, 'api/spa/index.html', {})

@login_required(login_url='login')
def other_spa_routes(request, path=None):
    return render(request, 'api/spa/index.html', {})

class FriendRequestViewSet(viewsets.ModelViewSet):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(
            models.Q(sender=self.request.user) | 
            models.Q(receiver=self.request.user)
        )

    @action(detail=False, methods=['get'])
    def pending(self, request):
        """Get all pending friend requests for the current user"""
        pending_requests = FriendRequest.objects.filter(
            receiver=request.user,
            status=FriendRequest.PENDING
        )
        serializer = self.get_serializer(pending_requests, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def friends(self, request):
        """Get all friends of the current user"""
        user = request.user
        friends = user.friends.all()
        serializer = UserProfileSerializer(friends, many=True)
        return Response(serializer.data)

    def create(self, request):
        receiver_id = request.data.get('receiver')
        if receiver_id == request.user.id:
            return Response(
                {'error': 'You cannot send a friend request to yourself'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if a friend request already exists
        existing_request = FriendRequest.objects.filter(
            (models.Q(sender=request.user) & models.Q(receiver=receiver_id)) |
            (models.Q(sender=receiver_id) & models.Q(receiver=request.user)),
            status=FriendRequest.PENDING
        ).first()

        if existing_request:
            return Response(
                {'error': 'A friend request already exists between these users'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if users are already friends
        if request.user.friends.filter(id=receiver_id).exists():
            return Response(
                {'error': 'Users are already friends'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data={
            'sender': request.user.id,
            'receiver': receiver_id
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        friend_request = self.get_object()
        if friend_request.receiver != request.user:
            return Response(
                {'error': 'You can only accept requests sent to you'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if friend_request.accept():
            return Response({'status': 'friend request accepted'})
        return Response(
            {'error': 'Friend request cannot be accepted'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        friend_request = self.get_object()
        if friend_request.receiver != request.user:
            return Response(
                {'error': 'You can only reject requests sent to you'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if friend_request.reject():
            return Response({'status': 'friend request rejected'})
        return Response(
            {'error': 'Friend request cannot be rejected'},
            status=status.HTTP_400_BAD_REQUEST
        )
