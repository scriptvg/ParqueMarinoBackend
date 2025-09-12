from django.urls import path
from apps.support.security.views import UserProfileViewSet, GroupViewSet, GroupPermissionsViewSet, LoginView, LogoutView, ForgotPasswordView, ResetPasswordConfirmView, RegisterView, Users_ViewSet, CurrentUserProfileView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apps.support.security.serializers import CustomTokenObtainPairSerializer

urlpatterns = [

    # Perfil de usuario actual
    path('profile/', CurrentUserProfileView.as_view(), name='current-user-profile'),

    # Perfil de usuario
    # Ruta para listar
    path('user_profile/', UserProfileViewSet.as_view({'get': 'list'}), name='user_profile-get'),

    # Ruta para crear
    path('user_profile/create/', UserProfileViewSet.as_view({'get': 'list', 'post': 'create'}), name='user_profile-list-create'),

    # Ruta para detalle
    path('user_profile/<int:pk>/', UserProfileViewSet.as_view({'get': 'retrieve'}), name='user_profile-detail'),

    # Ruta para actualizar o editar
    path('user_profile/<int:pk>/update/', UserProfileViewSet.as_view({'put': 'update'}), name='user_profile-update'),

    # Ruta para eliminar
    path('user_profile/<int:pk>/delete/', UserProfileViewSet.as_view({'delete': 'destroy'}), name='user_profile-delete'),


    # Roles
    # Ruta para listar
    path('roles/', GroupViewSet.as_view({'get': 'list'}), name='roles-get'),

    # Ruta para crear
    path('roles/create/', GroupViewSet.as_view({'get': 'list', 'post': 'create'}), name='roles-create'),

    # Ruta para detalle
    path('roles/<int:pk>/detail/', GroupViewSet.as_view({'get': 'list'}), name='roles-detail'),

    # Ruta para actualizar o editar
    path('roles/<int:pk>/update/', GroupViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name='roles-update'),

    # Ruta para eliminar
    path('roles/<int:pk>/delete/', GroupViewSet.as_view({'delete': 'destroy'}), name='roles-delete'),


    # Permissions
    # Ruta para listar
    path('permissions/', GroupPermissionsViewSet.as_view({'get': 'list'}), name='permissions-get'),

    # Ruta para crear
    path('permissions/<int:pk>/create/', GroupPermissionsViewSet.as_view({'get': 'list', 'post': 'create'}), name='permissions-create'),

    # Ruta para detalle
    path('permissions/<int:pk>/detail/', GroupPermissionsViewSet.as_view({'get': 'list'}), name='permissions-detail'),

    # Ruta para actualizar o editar
    path('permissions/<int:pk>/update/', GroupPermissionsViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name='permissions-update'),

    # Ruta para eliminar
    path('permissions/<int:pk>/delete/', GroupPermissionsViewSet.as_view({'delete': 'destroy'}), name='permissions-delete'),


    # Usuarios
    # Ruta para listar
    path('users/', Users_ViewSet.as_view({'get': 'list'}), name='users-get'),
    
    # Ruta para crear
    path('users/create/', Users_ViewSet.as_view({'get': 'list', 'post': 'create'}), name='users-create'),
    
    # Ruta para detalle
    path('users/<int:pk>/detail/', Users_ViewSet.as_view({'get': 'list'}), name='users-detail'),
    
    # Ruta para actualizar o editar
    path('users/<int:pk>/update/', Users_ViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name='users-update'),
    
    # Ruta para eliminar
    path('users/<int:pk>/delete/', Users_ViewSet.as_view({'delete': 'destroy'}), name='users-delete'),
    
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