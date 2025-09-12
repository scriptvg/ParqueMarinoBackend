from django.urls import path
from apps.support.security.views import LoginView, LogoutView, ForgotPasswordView, ResetPasswordConfirmView, RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apps.support.security.serializers import CustomTokenObtainPairSerializer

urlpatterns = [
    # Autenticacion y registro
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/', TokenObtainPairView.as_view(serializer_class=CustomTokenObtainPairSerializer), name='token_obtain_pair'),

    # Login/Logout/Register
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    # Password Reset
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password-confirm/', ResetPasswordConfirmView.as_view(), name='reset_password_confirm'),
]