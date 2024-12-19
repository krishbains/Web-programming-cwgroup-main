from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse
from . import views
from django.views.generic import TemplateView

from .views import main_spa

urlpatterns = [
    path('', main_spa),
    path('home/', TemplateView.as_view(template_name='api/spa/home.html'), name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
