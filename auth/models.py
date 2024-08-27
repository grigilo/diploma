from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

USER_ROLE_CHOICES = [("AD", "ADMIN"), ("US", "USER")]


class User(AbstractUser):
    REQUIRED_FIELDS = []
    objects = UserManager()
    USERNAME_FIELD = "email"

    first_name = models.CharField(max_length=128, null=True, blank=True)
    last_name = models.CharField(max_length=128, null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    email = models.EmailField(null=False, blank=False, unique=True)
    role = models.CharField(
        max_length=32, choices=USER_ROLE_CHOICES, default=USER_ROLE_CHOICES[1][0]
    )
    image = models.ImageField(upload_to="avatar", null=True)
    is_active = models.BooleanField(default=False)
    username = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
