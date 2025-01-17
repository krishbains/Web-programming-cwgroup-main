from typing import Optional, Dict, Any, Final

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class Hobby(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "hobbies"


class CustomUserManager(UserManager):
    def create_user(
            self,
            username: str,
            email: Optional[str] = None,
            password: Optional[str] = None,
            **extra_fields: Dict[str, Any]
    ) -> AbstractBaseUser:
        if not username:
            raise ValueError('The Username field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
            self,
            username: str,
            email: Optional[str] = None,
            password: Optional[str] = None,
            **extra_fields: Dict[str, Any]
    ) -> AbstractBaseUser:
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)
    hobbies = models.ManyToManyField(Hobby, related_name='users', blank=True)
    friends = models.ManyToManyField('self', blank=True, symmetrical=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']  # Add email as required for superusers

    def __str__(self) -> str:
        return self.username


class FriendRequest(models.Model):
    PENDING: Final[str] = 'pending'
    ACCEPTED: Final[str] = 'accepted'
    REJECTED: Final[str] = 'rejected'

    STATUS_CHOICES: Final[list[tuple[str, str]]] = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    ]

    sender = models.ForeignKey('CustomUser', related_name='sent_friend_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey('CustomUser', related_name='received_friend_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self) -> str:
        return f"{self.sender} -> {self.receiver} ({self.status})"

    def accept(self) -> bool:
        if self.status == self.PENDING:
            self.status = self.ACCEPTED
            self.save()
            self.sender.friends.add(self.receiver)
            return True
        return False

    def reject(self) -> bool:
        if self.status == self.PENDING:
            self.status = self.REJECTED
            self.save()
            return True
        return False
