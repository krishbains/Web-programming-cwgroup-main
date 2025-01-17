# ai/signals.py

from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password
from datetime import datetime
from ai.models import User  # Updated to use ai.models

@receiver(post_migrate)
def create_default_users(sender, **kwargs):
    # Only create users if there are none in the database
    if User.objects.count() == 0:
        default_users = [
            {
                'username': 'student1',
                'email': 'student1@university.com',
                'password': 'Student123!',
                'date_of_birth': '1995-05-15'
            },
            {
                'username': 'student2',
                'email': 'student2@university.com',
                'password': 'Student123!',
                'date_of_birth': '1997-08-22'
            },
            {
                'username': 'professor',
                'email': 'professor@university.com',
                'password': 'Prof123!',
                'date_of_birth': '1980-01-10'
            },
        ]

        for user_data in default_users:
            User.objects.create(
                username=user_data['username'],
                email=user_data['email'],
                password=make_password(user_data['password']),
                date_of_birth=datetime.strptime(user_data['date_of_birth'], '%Y-%m-%d').date()
            )
            print(f'Created default user: {user_data["username"]}')