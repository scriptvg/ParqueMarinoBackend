from django.urls import path
from apps.business.infrastructure.views import InfrastructureListAPIView

# Configuración de las rutas para la API de Infrastructure
# Cada ruta proporciona endpoints para operaciones CRUD en diferentes modelos

app_name = 'infrastructure'

urlpatterns = [
    # Resumen general de infraestructura
    path('summary/', InfrastructureListAPIView.as_view(), name='infrastructure-summary'),
    
    # Secciones - Gestión de secciones del parque
    path('sections/', InfrastructureListAPIView.as_view(), name='sections-list'),
    
    path('sections/<int:pk>/', InfrastructureListAPIView.as_view(), name='sections-detail'),
    
    # Hábitats de Infraestructura - Gestión de hábitats
    path('habitats/', InfrastructureListAPIView.as_view(), name='habitats-list'),
    
    path('habitats/<int:pk>/', InfrastructureListAPIView.as_view(), name='habitats-detail'),
]