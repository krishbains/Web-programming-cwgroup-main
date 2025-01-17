from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.http import HttpResponse
from . import views
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from .views import main_spa, HobbyViewSet, SimilarUserListView, UserProfileViewSet, register_view, login_view, logout_view

router = DefaultRouter()
router.register(r'hobbies', HobbyViewSet, basename='hobby')
router.register(r'profile', views.UserProfileViewSet, basename='profile')
router.register(r'friend-requests', views.FriendRequestViewSet, basename='friend-request')

urlpatterns = [
    # path('', main_spa),
    # path('home/', TemplateView.as_view(template_name='api/spa/home.html'), name='home'),
    path('admin/', admin.site.urls),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('api/', include(router.urls)),
    # path('api/similar-users/', SimilarUserListView.as_view(), name='similar-users'),
    # Serve the Vue SPA for all other routes
    re_path(r'^(?!api/).*$', views.other_spa_routes, name='other-routes'),
]
