from django.urls import path
from apps.business.education.views import ProgramaViewSet

# Configuración de rutas para el módulo de Programas
# Este módulo maneja toda la lógica relacionada con los programas educativos

app_name = 'programas'

urlpatterns = [
    # Listar - Obtiene todos los programas
    path(
        '',
        ProgramaViewSet.as_view({'get': 'list'}),
        name='programas-list'
    ),

    # Crear - Añade un nuevo programa
    path(
        'create/',
        ProgramaViewSet.as_view({'post': 'create'}),
        name='programas-create'
    ),

    # Detalle - Obtiene información detallada de un programa
    path(
        '<int:pk>/',
        ProgramaViewSet.as_view({'get': 'retrieve'}),
        name='programas-detail'
    ),

    # Actualizar - Modifica un programa existente
    path(
        '<int:pk>/update/',
        ProgramaViewSet.as_view({
            'put': 'update',
            'patch': 'partial_update'
        }),
        name='programas-update'
    ),

    # Eliminar - Elimina un programa
    path(
        '<int:pk>/delete/',
        ProgramaViewSet.as_view({'delete': 'destroy'}),
        name='programas-delete'
    ),
]