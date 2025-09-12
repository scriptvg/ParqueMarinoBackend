from django.urls import path
from apps.business.education.views import ProgramaItemViewSet

# Configuración de rutas para el módulo de Items de Programas
# Este módulo maneja toda la lógica relacionada con los items de programas educativos

app_name = 'programa_items'

urlpatterns = [
    # Listar - Obtiene todos los items de programas
    path(
        '',
        ProgramaItemViewSet.as_view({'get': 'list'}),
        name='programa-items-list'
    ),

    # Crear - Añade un nuevo item de programa
    path(
        'create/',
        ProgramaItemViewSet.as_view({'post': 'create'}),
        name='programa-items-create'
    ),

    # Detalle - Obtiene información detallada de un item de programa
    path(
        '<int:pk>/',
        ProgramaItemViewSet.as_view({'get': 'retrieve'}),
        name='programa-items-detail'
    ),

    # Actualizar - Modifica un item de programa existente
    path(
        '<int:pk>/update/',
        ProgramaItemViewSet.as_view({
            'put': 'update',
            'patch': 'partial_update'
        }),
        name='programa-items-update'
    ),

    # Eliminar - Elimina un item de programa
    path(
        '<int:pk>/delete/',
        ProgramaItemViewSet.as_view({'delete': 'destroy'}),
        name='programa-items-delete'
    ),
]