from django.urls import path
from apps.support.security.views import UserProfileViewSet, CurrentUserProfileView

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
]