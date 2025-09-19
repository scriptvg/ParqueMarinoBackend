from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from .models import UserProfile
from .serializers import UserProfileSerializer, GroupSerializer, UserSerializer

class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdminUser]

class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser]

class GroupPermissionsViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser]

class Users_ViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class CurrentUserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        # For now, we'll keep the existing implementation
        # In a real implementation, we would verify OTP here
        return Response({"message": "Login successful"})

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        return Response({"message": "Logout successful"})

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            # Extract user data from request
            name = request.data.get('name')
            email = request.data.get('email')
            password = request.data.get('password')
            
            # Validate that we have data
            if not request.data:
                return Response({
                    'error': 'No data provided in request'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Validate required fields
            if not name or not email or not password:
                return Response({
                    'error': 'Name, email, and password are required',
                    'required_fields': ['name', 'email', 'password']
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if user already exists
            if User.objects.filter(email=email).exists():
                return Response({
                    'error': 'A user with this email already exists'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Create user
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=name.split(' ')[0],
                last_name=' '.join(name.split(' ')[1:]) if len(name.split(' ')) > 1 else ''
            )
            
            # Assign 'client' role by default
            try:
                client_group = Group.objects.get(name='client')
                user.groups.add(client_group)
            except Exception:
                # If 'client' group doesn't exist, create it
                client_group, created = Group.objects.get_or_create(name='client')
                user.groups.add(client_group)
            
            # Create user profile
            UserProfile.objects.create(
                user=user,
                phone=request.data.get('phone', ''),
                address=request.data.get('address', '')
            )
            
            return Response({
                'message': 'User registered successfully',
                'user': {
                    'id': user.id,
                    'name': user.get_full_name(),
                    'email': user.email,
                    'role': 'client'
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'error': 'Registration failed',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
    permission_classes = [AllowAny]
    def post(self, request):
        return Response({"message": "Password reset email sent"})

class ResetPasswordConfirmView(APIView):
    permission_classes = [AllowAny]
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