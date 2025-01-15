from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from rest_framework import viewsets
from .forms import CustomUserCreationForm
from rest_framework.decorators import action
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Hobby
from .serializers import HobbySerializer, UserProfileSerializer
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import update_session_auth_hash



def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            api = form.save()
            login(request, api)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'api/spa/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            api = form.get_user()
            login(request, api)
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
    return render(request, 'api/spa/index.html', {})

@login_required(login_url='login')
def other_spa_routes(request, path=None):
    return render(request, 'api/spa/index.html', {})
