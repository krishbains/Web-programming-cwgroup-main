from typing import Optional, Dict, Any
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from django.db import transaction
from .forms import CustomUserCreationForm
from .models import Hobby
from .serializers import HobbySerializer, UserProfileSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import update_session_auth_hash


def register_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            api: User = form.save()
            login(request, api)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'api/spa/register.html', {'form': form})


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            api: User = form.get_user()
            login(request, api)
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'api/spa/login.html', {'form': form})


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('login')


class HobbyViewSet(viewsets.ModelViewSet):
    queryset = Hobby.objects.all()
    serializer_class = HobbySerializer
    permission_classes = [IsAuthenticated]

    def list(self, request: Request) -> Response:
        hobbies = self.get_queryset()
        user_hobby_ids = request.user.hobbies.values_list('id', flat=True)
        serializer = self.get_serializer(hobbies, many=True)
        data = serializer.data

        # Add a field to indicate if user has this hobby
        for hobby in data:
            hobby['user_has_hobby'] = hobby['id'] in user_hobby_ids

        return Response(data)

    @action(detail=True, methods=['post'])
    def add_to_profile(self, request: Request, pk: Optional[str] = None) -> Response:
        hobby: Hobby = self.get_object()
        request.user.hobbies.add(hobby)
        return Response({'status': 'hobby added to profile'})

    @action(detail=True, methods=['post'])
    def remove_from_profile(self, request: Request, pk: Optional[str] = None) -> Response:
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

        hobby, created = Hobby.objects.get_or_create(
            name=name,
            defaults={'name': name}
        )

        # Automatically add to user's profile when creating
        request.user.hobbies.add(hobby)

        data: Dict[str, Any] = {
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
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self) -> User:
        # Return the current authenticated user
        return self.request.user  # type: ignore

    @action(detail=False, methods=['get'])
    def me(self, request: Request) -> Response:
        # Get current user's profile
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request: Request) -> Response:
        user: User = self.get_object()
        is_partial: bool = request.method == 'PATCH'

        # Remove empty fields from request data
        cleaned_data: Dict[str, Any] = {
            k: v for k, v in request.data.items() if v is not None and v != ''
        }

        serializer = self.get_serializer(
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
    return render(request, 'api/spa/index.html', {})


@login_required(login_url='login')
def other_spa_routes(request: HttpRequest, path: Optional[str] = None) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})
