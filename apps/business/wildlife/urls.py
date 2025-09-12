from django.urls import path
from apps.business.wildlife.views import (
    ConservationStatusViewSet,
    SpecieViewSet,
    AnimalViewSet,
    HabitatViewSet
)

# Configuración de las rutas para la API de Wildlife (Vida Silvestre)
# Cada ruta proporciona endpoints para operaciones CRUD en diferentes modelos

app_name = 'wildlife'

urlpatterns = [
    # Estados de conservación - Gestión de clasificaciones IUCN y CITES
    path('conservation-status/', ConservationStatusViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='conservation-status-list-create'),
    
    path('conservation-status/<int:pk>/', ConservationStatusViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='conservation-status-detail'),

    # Especies - Catálogo de especies marinas
    path('species/', SpecieViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='species-list-create'),
    
    path('species/<int:pk>/', SpecieViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='species-detail'),

    # Animales - Registros individuales de animales
    path('animals/', AnimalViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='animals-list-create'),
    
    path('animals/<int:pk>/', AnimalViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='animals-detail'),

    # Hábitats - Ecosistemas marinos
    path('habitats/', HabitatViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='habitats-list-create'),
    
    path('habitats/<int:pk>/', HabitatViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='habitats-detail'),
]