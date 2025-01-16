from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from rest_framework import viewsets, generics
from .forms import CustomUserCreationForm
from rest_framework.decorators import action
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Hobby, CustomUser
from .serializers import HobbySerializer, UserProfileSerializer
from django.http import JsonResponse
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter


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

        serializer = self.get_serializer(
            user,
            data=request.data,
            partial=is_partial
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserFilter(filters.FilterSet):
    min_age = filters.NumberFilter(field_name='date_of_birth', lookup_expr='lte', method='filter_by_age')
    max_age = filters.NumberFilter(field_name='date_of_birth', lookup_expr='gte', method='filter_by_age')

    class Meta:
        model = CustomUser
        fields = ['min_age', 'max_age']

    def filter_by_age(self, queryset, name, value):
        from datetime import date
        today = date.today()
        if name == 'min_age':
            return queryset.filter(date_of_birth__lte=today.replace(year=today.year - value))
        if name == 'max_age':
            return queryset.filter(date_of_birth__gte=today.replace(year=today.year - value))
        return queryset

    
class SimilarUserListView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = UserFilter
    ordering = ['-similarity_score']

    def get_queryset(self):
        current_user = self.request.user
        queryset = CustomUser.objects.exclude(id=current_user.id)
        return sorted(queryset, key=lambda user: current_user.similarity_score(user), reverse=True)


@login_required(login_url='login')
def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})

@login_required(login_url='login')
def other_spa_routes(request, path=None):
    return render(request, 'api/spa/index.html', {})
