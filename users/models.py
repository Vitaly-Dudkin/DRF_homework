from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    username = None

    email = models.EmailField(unique=True, verbose_name='email')
    phone = models.CharField(null=True, blank=True, max_length=50, verbose_name='Phone')
    city = models.CharField(null=True, blank=True, max_length=50, verbose_name='City')
    avatar = models.ImageField(null=True, blank=True, upload_to='', verbose_name='Photo')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
