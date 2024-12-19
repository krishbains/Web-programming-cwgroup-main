
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse


urlpatterns = [
    path('', include('api.urls')),
    path('health', lambda request: HttpResponse("OK")),
    path('admin/', admin.site.urls),
]
