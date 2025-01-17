from typing import Dict, Union, Optional, List, Any

from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db import models, transaction
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from datetime import date, timedelta
from rest_framework.request import Request
from rest_framework.serializers import ModelSerializer

from .forms import CustomUserCreationForm
from .models import CustomUser, Hobby, FriendRequest
from .serializers import HobbySerializer, UserProfileSerializer, FriendRequestSerializer



def register_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            api = form.save()
            login(request, api)
            return redirect('/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'api/spa/register.html', {'form': form})

def login_view(request: HttpRequest) -> HttpResponse:
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

def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('login')


class HobbyViewSet(viewsets.ModelViewSet):
    queryset: QuerySet[Hobby] = Hobby.objects.all()
    serializer_class: type[HobbySerializer] = HobbySerializer
    permission_classes: list[type[IsAuthenticated]] = [IsAuthenticated]

    def list(self, request: Request) -> Response:
        # Get all hobbies and mark which ones the user has
        hobbies: QuerySet[Hobby] = self.get_queryset()
        user_hobby_ids: QuerySet[int] = request.user.hobbies.values_list('id', flat=True)

        serializer: ModelSerializer = self.get_serializer(hobbies, many=True)
        data: List[Dict[str, Any]] = serializer.data

        # Add a field to indicate if user has this hobby
        for hobby in data:
            hobby['user_has_hobby'] = hobby['id'] in user_hobby_ids

        return Response(data)

    @action(detail=True, methods=['post'])
    def add_to_profile(self, request: Request, pk: Optional[int] = None) -> Response:
        hobby: Hobby = self.get_object()
        request.user.hobbies.add(hobby)
        return Response({'status': 'hobby added to profile'})

    @action(detail=True, methods=['post'])
    def remove_from_profile(self, request: Request, pk: Optional[int] = None) -> Response:
        hobby: Hobby = self.get_object()
        request.user.hobbies.remove(hobby)
        return Response({'status': 'hobby removed from profile'})

    @action(detail=False, methods=['post'])
    @transaction.atomic
    def create_hobby(self, request: Request) -> Response:
        name: str = request.data.get('name', '').lower().strip()

        if not name:
            return Response(
                {'error': 'Name is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        hobby: Hobby
        created: bool
        hobby, created = Hobby.objects.get_or_create(
            name=name,
            defaults={'name': name}
        )

        # Automatically add to user's profile when creating
        request.user.hobbies.add(hobby)

        data: Dict[str, Union[int, str, bool]] = {
            'id': hobby.id,
            'name': hobby.name,
            'created': created,
            'user_has_hobby': True
        }

        return Response(
            data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )

@method_decorator(ensure_csrf_cookie, name='dispatch')
class UserProfileViewSet(viewsets.GenericViewSet):
    serializer_class: type[UserProfileSerializer] = UserProfileSerializer
    permission_classes: list[type[IsAuthenticated]] = [IsAuthenticated]

    def get_object(self) -> CustomUser:
        # Return the current authenticated user
        return self.request.user

    @action(detail=False, methods=['get'])
    def me(self, request: Request) -> Response:
        # Get current user's profile
        serializer: UserProfileSerializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search_users(self, request: Request) -> Response:
        """Search for users with similar hobbies and optional age filtering."""
        try:
            # Get query parameters
            min_age: Optional[str] = request.query_params.get('min_age')
            max_age: Optional[str] = request.query_params.get('max_age')
            page: int = int(request.query_params.get('page', 1))
            per_page: int = 10  # Fixed page size

            # Get current user's hobbies
            user_hobbies: models.QuerySet = request.user.hobbies.all()

            # Base queryset excluding the current user
            queryset: models.QuerySet[CustomUser] = CustomUser.objects.exclude(id=request.user.id)

            # Filter users who have at least one hobby in common
            if user_hobbies:
                queryset = queryset.filter(hobbies__in=user_hobbies).distinct()

            # Apply age filters if provided
            if min_age or max_age:
                today: date = date.today()

                if min_age:
                    try:
                        max_date: date = today - timedelta(days=int(min_age) * 365)
                        queryset = queryset.filter(date_of_birth__lte=max_date)
                    except ValueError:
                        return Response(
                            {'error': 'Invalid minimum age value'},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                if max_age:
                    try:
                        min_date: date = today - timedelta(days=(int(max_age) + 1) * 365)
                        queryset = queryset.filter(date_of_birth__gt=min_date)
                    except ValueError:
                        return Response(
                            {'error': 'Invalid maximum age value'},
                            status=status.HTTP_400_BAD_REQUEST
                        )

            # Calculate hobby similarity and annotate the queryset
            queryset = queryset.annotate(
                common_hobbies_count=models.Count(
                    'hobbies',
                    filter=models.Q(hobbies__in=user_hobbies)
                )
            ).order_by('-common_hobbies_count')

            # Implement pagination
            total_users: int = queryset.count()
            total_pages: int = (total_users + per_page - 1) // per_page

            # Validate page number
            if page < 1:
                page = 1
            elif page > total_pages and total_pages > 0:
                page = total_pages

            start: int = (page - 1) * per_page
            end: int = start + per_page
            users_page: List[CustomUser] = list(queryset[start:end])

            # Serialize the results
            serializer: UserProfileSerializer = self.get_serializer(users_page, many=True)
            data: List[Dict[str, Any]] = serializer.data

            # Add the common hobbies count, age, and friendship status to each user
            today = date.today()
            for user_data, user_obj in zip(data, users_page):
                user_data['common_hobbies_count'] = user_obj.common_hobbies_count

                # Add age
                if user_obj.date_of_birth:
                    age: int = today.year - user_obj.date_of_birth.year
                    if today.month < user_obj.date_of_birth.month or (
                            today.month == user_obj.date_of_birth.month and
                            today.day < user_obj.date_of_birth.day
                    ):
                        age -= 1
                    user_data['age'] = age

                # Check if users are friends
                user_data['is_friend'] = request.user.friends.filter(id=user_obj.id).exists()

                # Check for pending friend requests
                pending_request: Optional[FriendRequest] = FriendRequest.objects.filter(
                    (models.Q(sender=request.user) & models.Q(receiver=user_obj)) |
                    (models.Q(sender=user_obj) & models.Q(receiver=request.user)),
                    status=FriendRequest.PENDING
                ).first()
                user_data['has_pending_request'] = bool(pending_request)

            return Response({
                'users': data,
                'total_users': total_users,
                'total_pages': total_pages,
                'current_page': page
            })

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request: Request) -> Response:
        user: CustomUser = self.get_object()
        is_partial: bool = request.method == 'PATCH'

        # Remove empty fields from request data
        cleaned_data: Dict[str, Any] = {
            k: v for k, v in request.data.items()
            if v is not None and v != ''
        }

        serializer: UserProfileSerializer = self.get_serializer(
            user,
            data=cleaned_data,
            partial=is_partial
        )

        if serializer.is_valid():
            # Check if only password is being updated
            is_password_only_update: bool = set(cleaned_data.keys()).issubset(
                {'current_password', 'new_password'}
            )

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
def other_spa_routes(request: HttpRequest, path: Optional[str] = None) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})

class FriendRequestViewSet(viewsets.ModelViewSet):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet[FriendRequest]:
        return FriendRequest.objects.filter(
            models.Q(sender=self.request.user) |
            models.Q(receiver=self.request.user)
        )

    @action(detail=False, methods=['get'])
    def pending(self, request: Request) -> Response:
        """Get all pending friend requests for the current user"""
        pending_requests: QuerySet[FriendRequest] = FriendRequest.objects.filter(
            receiver=request.user,
            status=FriendRequest.PENDING
        )
        serializer = self.get_serializer(pending_requests, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def friends(self, request: Request) -> Response:
        """Get all friends of the current user"""
        user: CustomUser = request.user
        friends: QuerySet[CustomUser] = user.friends.all()
        serializer = UserProfileSerializer(friends, many=True)
        return Response(serializer.data)

    def create(self, request: Request) -> Response:
        try:
            receiver_id: Optional[int] = request.data.get('receiver')
            if not receiver_id:
                return Response(
                    {'error': 'Receiver ID is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                receiver: CustomUser = CustomUser.objects.get(id=receiver_id)
            except CustomUser.DoesNotExist:
                return Response(
                    {'error': 'Receiver user not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

            if receiver_id == request.user.id:
                return Response(
                    {'error': 'You cannot send a friend request to yourself'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if request.user.friends.filter(id=receiver_id).exists():
                return Response(
                    {'error': 'Users are already friends'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            existing_request: Optional[FriendRequest] = FriendRequest.objects.filter(
                models.Q(sender=request.user, receiver=receiver) |
                models.Q(sender=receiver, receiver=request.user)
            ).first()

            if existing_request:
                if existing_request.status == FriendRequest.PENDING:
                    return Response(
                        {'error': 'A friend request already exists between these users'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                elif existing_request.status == FriendRequest.REJECTED:
                    existing_request.status = FriendRequest.PENDING
                    existing_request.save()
                    serializer = self.get_serializer(existing_request)
                    return Response(serializer.data, status=status.HTTP_200_OK)

            friend_request: FriendRequest = FriendRequest.objects.create(
                sender=request.user,
                receiver=receiver,
                status=FriendRequest.PENDING
            )

            serializer = self.get_serializer(friend_request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def accept(self, request: Request, pk: Optional[int] = None) -> Response:
        friend_request: FriendRequest = self.get_object()
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
    def reject(self, request: Request, pk: Optional[int] = None) -> Response:
        friend_request: FriendRequest = self.get_object()
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

    @action(detail=False, methods=['post'])
    def unfollow(self, request: Request) -> Response:
        """Remove a user from friends list"""
        user_id: Optional[int] = request.data.get('user_id')
        if not user_id:
            return Response(
                {'error': 'user_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            friend: CustomUser = CustomUser.objects.get(id=user_id)

            request.user.friends.remove(friend)

            FriendRequest.objects.filter(
                (models.Q(sender=request.user) & models.Q(receiver=friend)) |
                (models.Q(sender=friend) & models.Q(receiver=request.user))
            ).delete()

            return Response({'status': 'user unfollowed'})
        except CustomUser.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
