from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from datetime import datetime
import re



class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=8, write_only=True)
    password2 = serializers.CharField(max_length=68, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'first_name', 'last_name', 'phone_number', 'birthdate']

    def validate(self, attrs):
        if "@" not in attrs.get('email', '') or "." not in attrs.get('email', ''):
            raise serializers.ValidationError(_("Invalid Email."))
        if attrs.get('phone_number', '') != '':
            if not re.match(r'^\d{9,15}$', attrs.get('phone_number', '')):
                raise serializers.ValidationError(_("Phone number must contain only numbers and be between 9 and 15 digits."))
        # if attrs.get('birthdate', '') != '':
        #     try:
        #         datetime.strptime(attrs.get('birthdate', ''), "%d/%m/%Y")
        #     except ValueError:
        #         raise serializers.ValidationError(_("Ingresa la fecha de nacimiento en formato dd/mm/yyyy."))
        password = attrs.get('password', '')
        password2 = attrs.get('password2', '')
        if not re.match(r'^(?=.*[A-Z])(?=.*\d).{8,68}$', password):
            raise serializers.ValidationError(_("Password must contain at least 8 characters, including uppercase letters and numbers."))
        if password != password2:
            raise serializers.ValidationError(_("Passwords do not match."))
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number'],
            birthdate=validated_data['birthdate']
        )
        return user
    
    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=8, write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'password']
    
    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        
        user = authenticate(email=email, password=password)
        
        if not user:
            raise ValueError('Incorrect email or password')
        
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'birthdate']
        
        
class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(max_length=68, min_length=8, write_only=True, required=True)
    new_password = serializers.CharField(max_length=68, min_length=8, write_only=True, required=True)
    confirm_password = serializers.CharField(max_length=68, min_length=8, write_only=True, required=True)
    

    
