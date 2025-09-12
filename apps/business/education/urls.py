from django.urls import path
from apps.business.education.views import (
    InstructorViewSet, ProgramaViewSet, HorarioViewSet, InscripcionViewSet,
    ServiciosEducativosViewSet, ServiciosEducativosImageViewSet,
    ServiciosEducativosFactsViewSet, ServiciosEducativosDescriptionViewSet,
    ServiciosEducativosButtonsViewSet, ProgramaEducativoViewSet, ProgramaItemViewSet
)

# Configuración de las rutas para la API de Education (Educación)
# Cada ruta proporciona endpoints para operaciones CRUD en diferentes modelos

app_name = 'education'

urlpatterns = [
    # Instructores - Gestión de instructores del parque
    path('instructores/', InstructorViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='instructores-list-create'),
    
    path('instructores/<int:pk>/', InstructorViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='instructores-detail'),

    # Programas - Gestión de programas educativos
    path('programas/', ProgramaViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='programas-list-create'),
    
    path('programas/<int:pk>/', ProgramaViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='programas-detail'),

    # Horarios - Gestión de horarios de programas
    path('horarios/', HorarioViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='horarios-list-create'),
    
    path('horarios/<int:pk>/', HorarioViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='horarios-detail'),

    # Inscripciones - Gestión de inscripciones a programas
    path('inscripciones/', InscripcionViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='inscripciones-list-create'),
    
    path('inscripciones/<int:pk>/', InscripcionViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='inscripciones-detail'),

    # Servicios Educativos - Gestión de servicios educativos
    path('servicios/', ServiciosEducativosViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='servicios-educativos-list-create'),
    
    path('servicios/<int:pk>/', ServiciosEducativosViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='servicios-educativos-detail'),

    # Imágenes de Servicios - Gestión de imágenes de servicios educativos
    path('servicios-imagenes/', ServiciosEducativosImageViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='servicios-educativos-images-list-create'),
    
    path('servicios-imagenes/<int:pk>/', ServiciosEducativosImageViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='servicios-educativos-images-detail'),

    # Datos de Servicios - Gestión de datos de servicios educativos
    path('servicios-facts/', ServiciosEducativosFactsViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='servicios-educativos-facts-list-create'),
    
    path('servicios-facts/<int:pk>/', ServiciosEducativosFactsViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='servicios-educativos-facts-detail'),

    # Descripciones de Servicios - Gestión de descripciones de servicios educativos
    path('servicios-descripciones/', ServiciosEducativosDescriptionViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='servicios-educativos-descriptions-list-create'),
    
    path('servicios-descripciones/<int:pk>/', ServiciosEducativosDescriptionViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='servicios-educativos-descriptions-detail'),

    # Botones de Servicios - Gestión de botones de servicios educativos
    path('servicios-botones/', ServiciosEducativosButtonsViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='servicios-educativos-buttons-list-create'),
    
    path('servicios-botones/<int:pk>/', ServiciosEducativosButtonsViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='servicios-educativos-buttons-detail'),

    # Programas Educativos - Gestión de programas educativos
    path('programas-educativos/', ProgramaEducativoViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='programas-educativos-list-create'),
    
    path('programas-educativos/<int:pk>/', ProgramaEducativoViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='programas-educativos-detail'),

    # Items de Programas - Gestión de items de programas educativos
    path('programas-items/', ProgramaItemViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='programas-items-list-create'),
    
    path('programas-items/<int:pk>/', ProgramaItemViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='programas-items-detail'),
]