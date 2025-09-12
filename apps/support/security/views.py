from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from .models import UserProfile
from .serializers import UserProfileSerializer, GroupSerializer, UserSerializer

class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

class GroupPermissionsViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

class Users_ViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class CurrentUserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)

class LoginView(APIView):
    def post(self, request):
        # For now, we'll keep the existing implementation
        # In a real implementation, we would verify OTP here
        return Response({"message": "Login successful"})

class LogoutView(APIView):
    def post(self, request):
        return Response({"message": "Logout successful"})

class RegisterView(APIView):
    def post(self, request):
        # For now, we'll keep the existing implementation
        # In a real implementation, we would verify OTP here
        return Response({"message": "Registration successful"})

    def validate_otp_during_registration(self, phone_number, otp_code, user):
        """
        Helper method to validate OTP during registration
        This would be called when a user is registering with phone verification
        """
        from apps.support.messaging.services.twilio_service import TwilioService
        twilio_service = TwilioService()
        is_valid, message = twilio_service.verify_otp(phone_number, otp_code, user, 'registration')
        return is_valid, message

class ForgotPasswordView(APIView):
    def post(self, request):
        return Response({"message": "Password reset email sent"})

class ResetPasswordConfirmView(APIView):
    def post(self, request):
        return Response({"message": "Password reset successful"})

class ChangePasswordView(APIView):
    """
    Vista para cambiar la contraseña del usuario autenticado.
    
    Características:
    - Requiere autenticación
    - Valida contraseña actual
    - Actualiza a nueva contraseña
    - Manejo de errores detallado
    
    Endpoint:
    POST /auth/change-password/
    
    Datos requeridos:
    - old_password: Contraseña actual
    - new_password: Nueva contraseña
    
    Respuestas:
    - 200: Contraseña actualizada exitosamente
    - 400: Error en validación
    - 401: No autenticado
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Procesa la solicitud de cambio de contraseña.
        
        Args:
            request: Solicitud HTTP con contraseñas
            
        Returns:
            Response: Mensaje de éxito o error
        """
        try:
            # Validar datos requeridos
            old_password = request.data.get('old_password')
            new_password = request.data.get('new_password')
            
            if not old_password or not new_password:
                return Response({
                    'error': 'Se requieren contraseña actual y nueva',
                    'required_fields': ['old_password', 'new_password']
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Validar contraseña actual
            user = request.user
            if not user.check_password(old_password):
                return Response({
                    'error': 'Contraseña actual incorrecta'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Validar nueva contraseña
            if len(new_password) < 8:
                return Response({
                    'error': 'La nueva contraseña debe tener al menos 8 caracteres'
                }, status=status.HTTP_400_BAD_REQUEST)
                
            if old_password == new_password:
                return Response({
                    'error': 'La nueva contraseña debe ser diferente a la actual'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Actualizar contraseña
            user.set_password(new_password)
            user.save()
            
            return Response({
                'message': 'Contraseña actualizada exitosamente',
                'user_id': user.id
            })
            
        except Exception as e:
            return Response({
                'error': 'Error al cambiar contraseña',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
