from django.contrib.auth.models import BaseUserManager
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class CustomUserManager(BaseUserManager):
    def email_validatior(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError("Email inválido")
    def create_user(self, email, password, **extra_fields):
        if email: 
            email = self.normalize_email(email)
            self.email_validatior(email)
        else: 
            raise ValueError("El campo de Email es obligatorio")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True")
        if extra_fields.get('is_verified') is not True:
            raise ValueError("Superuser must have is_verified=True")
        
        user = self.create_user(email, password, **extra_fields)
        user.save(using=self._db)
        return user
