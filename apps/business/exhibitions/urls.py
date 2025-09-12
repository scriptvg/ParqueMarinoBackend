from django.urls import path
from apps.business.exhibitions.views import (
    ExhibicionViewSet,
    ExhibicionImageViewSet,
    ExhibicionFactsViewSet,
    ExhibicionDescriptionViewSet,
    ExhibicionButtonsViewSet
)

# Configuración de las rutas para la API de Exhibitions (Exhibiciones)
# Cada ruta proporciona endpoints para operaciones CRUD en diferentes modelos

app_name = 'exhibitions'

urlpatterns = [
    # Exhibiciones - Gestión de exhibiciones del parque
    path('exhibitions/', ExhibicionViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='exhibitions-list-create'),
    
    path('exhibitions/<int:pk>/', ExhibicionViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='exhibitions-detail'),

    # Imágenes - Gestión de imágenes de exhibiciones
    path('images/', ExhibicionImageViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='exhibicion-images-list-create'),
    
    path('images/<int:pk>/', ExhibicionImageViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='exhibicion-images-detail'),

    # Datos - Gestión de datos interesantes de exhibiciones
    path('facts/', ExhibicionFactsViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='exhibicion-facts-list-create'),
    
    path('facts/<int:pk>/', ExhibicionFactsViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='exhibicion-facts-detail'),

    # Descripciones - Gestión de descripciones de exhibiciones
    path('descriptions/', ExhibicionDescriptionViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='exhibicion-descriptions-list-create'),
    
    path('descriptions/<int:pk>/', ExhibicionDescriptionViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='exhibicion-descriptions-detail'),

    # Botones - Gestión de botones de exhibiciones
    path('buttons/', ExhibicionButtonsViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='exhibicion-buttons-list-create'),
    
    path('buttons/<int:pk>/', ExhibicionButtonsViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='exhibicion-buttons-detail'),
]