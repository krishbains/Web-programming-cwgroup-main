from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.http import HttpResponse
from . import views
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from .views import main_spa, HobbyViewSet

router = DefaultRouter()
router.register(r'hobbies', HobbyViewSet, basename='hobby')
router.register(r'profile', views.UserProfileViewSet, basename='profile')
router.register(r'friend-requests', views.FriendRequestViewSet, basename='friend-request')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('api/', include(router.urls)),
    # Serve the Vue SPA for all other routes
    re_path(r'^.*$', views.main_spa, name='main-spa'),
]
