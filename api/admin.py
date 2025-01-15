from django.contrib import admin
from .models import CustomUser, Hobby

@admin.register(Hobby)
class HobbyAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_of_birth', 'is_staff')
    search_fields = ('username', 'email')
    filter_horizontal = ('hobbies',)  # Makes it easier to manage many-to-many relationships
    list_filter = ('is_staff', 'is_superuser', 'date_of_birth')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('date_of_birth', 'hobbies')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )