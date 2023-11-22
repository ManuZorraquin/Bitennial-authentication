from django.shortcuts import render
from rest_framework.generics import GenericAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserProfileSerializer, ChangePasswordSerializer
from .models import User
from rest_framework.response import Response
from rest_framework import status



class RegisterUserView(GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        print(serializer)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.data
            return Response({"status": "success", "message": "User created successfuly", "data": user}, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    
class LoginView(GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        try: 
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token

            data = {
                'refresh_token': str(refresh),
                'access_token': str(access),
            }

            return Response({"status": "success", "message": "Successful login", "data": data}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"data": None, "status": "error", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
class UserProfileView(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Response({"status": "success", "message": "User retrieved successfuly", "data": self.request.user}, status=status.HTTP_200_OK)
    
class UpdateUserProfileView(UpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Response({"status": "success", "message": "User updated successfuly", "data": self.request.user}, status=status.HTTP_200_OK)
    

class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def put(self, request):
        user = self.get_object()
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            current_password = serializer.validated_data.get('current_password')
            new_password = serializer.validated_data.get('new_password')
            confirm_password = serializer.validated_data.get('confirm_password')

            if not user.check_password(current_password):
                return Response({'message': 'Current password is incorrect', "status": "error"}, status=status.HTTP_400_BAD_REQUEST)

            if new_password != confirm_password:
                return Response({'message': 'New passwords do not match', "status": "error"}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()

            return Response({'message': 'Password updated succesfuly', "status": "success"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)