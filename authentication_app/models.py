from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .manager import CustomUserManager
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re
from datetime import datetime

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True, help_text="Formato: dd/mm/yyyy")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    
    objects = CustomUserManager()
