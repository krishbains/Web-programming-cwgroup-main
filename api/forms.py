from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'date_of_birth']

    def save(self, commit: bool = True) -> CustomUser:
        user: CustomUser = super().save(commit=False)
        if commit:
            user.save()
        return user
