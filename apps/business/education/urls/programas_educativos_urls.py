from django.urls import path
from apps.business.education.views import ProgramaEducativoViewSet

# Configuración de rutas para el módulo de Programas Educativos
# Este módulo maneja toda la lógica relacionada con los programas educativos del parque

app_name = 'programas_educativos'

urlpatterns = [
    # Listar - Obtiene todos los programas educativos
    path(
        '',
        ProgramaEducativoViewSet.as_view({'get': 'list'}),
        name='programas-educativos-list'
    ),

    # Crear - Añade un nuevo programa educativo
    path(
        'create/',
        ProgramaEducativoViewSet.as_view({'post': 'create'}),
        name='programas-educativos-create'
    ),

    # Detalle - Obtiene información detallada de un programa educativo
    path(
        '<int:pk>/',
        ProgramaEducativoViewSet.as_view({'get': 'retrieve'}),
        name='programas-educativos-detail'
    ),

    # Actualizar - Modifica un programa educativo existente
    path(
        '<int:pk>/update/',
        ProgramaEducativoViewSet.as_view({
            'put': 'update',
            'patch': 'partial_update'
        }),
        name='programas-educativos-update'
    ),

    # Eliminar - Elimina un programa educativo
    path(
        '<int:pk>/delete/',
        ProgramaEducativoViewSet.as_view({'delete': 'destroy'}),
        name='programas-educativos-delete'
    ),
]