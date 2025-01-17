from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password
from datetime import datetime, timedelta
from api.models import CustomUser, Hobby


@receiver(post_migrate)
def create_default_data(sender, **kwargs):
    if Hobby.objects.count() == 0:
        default_hobbies = [
            'Reading', 'Gaming', 'Sports', 'Music', 'Cooking',
            'Photography', 'Painting', 'Traveling', 'Writing',
            'Dancing'
        ]
        hobby_objects = []
        for hobby_name in default_hobbies:
            hobby = Hobby.objects.create(name=hobby_name)
            hobby_objects.append(hobby)
            print(f'Created hobby: {hobby_name}')

    if CustomUser.objects.count() == 0:
        default_users = [
            {
                'username': 'admin',
                'email': 'admin@admin.com',
                'password': 'admin',
                'date_of_birth': '1990-01-01',
                'hobbies': ['Reading', 'Gaming'],
                'is_staff': True,
                'is_superuser': True
            },
            {
                'username': 'student1',
                'email': 'student1@university.com',
                'password': 'Student123!',
                'date_of_birth': '1995-05-15',
                'hobbies': ['Reading', 'Gaming']
            },
            {
                'username': 'student2',
                'email': 'student2@university.com',
                'password': 'Student123!',
                'date_of_birth': '1997-08-22',
                'hobbies': ['Sports', 'Music']
            },
            {
                'username': 'professor',
                'email': 'professor@university.com',
                'password': 'Prof123!',
                'date_of_birth': '1980-01-10',
                'hobbies': ['Reading', 'Cooking']
            },
            # Additional users
            {
                'username': 'alex_smith',
                'email': 'alex.smith@university.com',
                'password': 'Pass123!',
                'date_of_birth': '1996-03-12',
                'hobbies': ['Gaming', 'Music', 'Photography']
            },
            {
                'username': 'emma_wilson',
                'email': 'emma.w@university.com',
                'password': 'Pass123!',
                'date_of_birth': '1998-07-25',
                'hobbies': ['Painting', 'Photography', 'Writing']
            },
            {
                'username': 'james_brown',
                'email': 'j.brown@university.com',
                'password': 'Pass123!',
                'date_of_birth': '1995-11-30',
                'hobbies': ['Sports', 'Gaming']
            },
            {
                'username': 'sophia_lee',
                'email': 'sophia.lee@university.com',
                'password': 'Pass123!',
                'date_of_birth': '1997-04-18',
                'hobbies': ['Dancing', 'Music', 'Photography']
            },
            {
                'username': 'lucas_martinez',
                'email': 'l.martinez@university.com',
                'password': 'Pass123!',
                'date_of_birth': '1996-09-05',
                'hobbies': ['Cooking', 'Photography', 'Traveling']
            },
            {
                'username': 'olivia_taylor',
                'email': 'o.taylor@university.com',
                'password': 'Pass123!',
                'date_of_birth': '1999-01-15',
                'hobbies': ['Writing', 'Reading', 'Painting']
            },
            {
                'username': 'william_anderson',
                'email': 'w.anderson@university.com',
                'password': 'Pass123!',
                'date_of_birth': '1997-06-22',
                'hobbies': ['Sports', 'Gaming', 'Music']
            },
            {
                'username': 'ava_garcia',
                'email': 'ava.g@university.com',
                'password': 'Pass123!',
                'date_of_birth': '1998-12-03',
                'hobbies': ['Dancing', 'Photography', 'Music']
            },
            {
                'username': 'ethan_wright',
                'email': 'e.wright@university.com',
                'password': 'Pass123!',
                'date_of_birth': '1996-02-28',
                'hobbies': ['Gaming', 'Cooking', 'Reading']
            },
            {
                'username': 'isabella_kim',
                'email': 'i.kim@university.com',
                'password': 'Pass123!',
                'date_of_birth': '1997-10-14',
                'hobbies': ['Painting', 'Music', 'Traveling']
            },
            {
                'username': 'mason_thompson',
                'email': 'm.thompson@university.com',
                'password': 'Pass123!',
                'date_of_birth': '1995-08-09',
                'hobbies': ['Sports', 'Photography', 'Gaming']
            },
            {
                'username': 'chloe_martin',
                'email': 'c.martin@university.com',
                'password': 'Pass123!',
                'date_of_birth': '1998-04-27',
                'hobbies': ['Writing', 'Reading', 'Music']
            },
            {
                'username': 'daniel_lopez',
                'email': 'd.lopez@university.com',
                'password': 'Pass123!',
                'date_of_birth': '1996-11-19',
                'hobbies': ['Cooking', 'Dancing', 'Traveling']
            },
            {
                'username': 'aria_patel',
                'email': 'a.patel@university.com',
                'password': 'Pass123!',
                'date_of_birth': '1999-03-08',
                'hobbies': ['Photography', 'Painting', 'Writing']
            },
            {
                'username': 'henry_wilson',
                'email': 'h.wilson@university.com',
                'password': 'Pass123!',
                'date_of_birth': '1997-07-16',
                'hobbies': ['Sports', 'Reading', 'Music']
            },
            {
                'username': 'zoe_chen',
                'email': 'z.chen@university.com',
                'password': 'Pass123!',
                'date_of_birth': '1998-05-31',
                'hobbies': ['Dancing', 'Gaming', 'Photography']
            },
            {
                'username': 'leo_rodriguez',
                'email': 'l.rodriguez@university.com',
                'password': 'Pass123!',
                'date_of_birth': '1925-12-24',
                'hobbies': ['Traveling', 'Cooking', 'Sports']
            }
        ]

        for user_data in default_users:
            # Extract hobbies from user data
            hobby_names = user_data.pop('hobbies')

            # Create user with optional staff and superuser status
            user = CustomUser.objects.create(
                username=user_data['username'],
                email=user_data['email'],
                password=make_password(user_data['password']),
                date_of_birth=datetime.strptime(user_data['date_of_birth'], '%Y-%m-%d').date(),
                is_staff=user_data.get('is_staff', False),
                is_superuser=user_data.get('is_superuser', False)
            )

            # Add hobbies to user
            hobbies = Hobby.objects.filter(name__in=hobby_names)
            user.hobbies.add(*hobbies)

            print(f'Created user: {user_data["username"]} with hobbies: {", ".join(hobby_names)}')