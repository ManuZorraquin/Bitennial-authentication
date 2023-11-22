from django.urls import path
from authentication_app import views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('edit-profile/', views.UpdateUserProfileView.as_view(), name='edit-profile'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]