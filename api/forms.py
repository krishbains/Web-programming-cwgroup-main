from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'date_of_birth']

        def save(self, commit=True):
            user = super().save(commit=False)
            user.save()
            return user