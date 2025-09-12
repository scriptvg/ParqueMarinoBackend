from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.support.security.permissions import IsAuthenticatedAndRole
from .models import (
    Exhibicion,
    ExhibicionImage,
    ExhibicionFacts,
    ExhibicionDescription,
    ExhibicionButtons
)
from .serializers import (
    ExhibicionSerializer,
    ExhibicionImageSerializer,
    ExhibicionFactsSerializer,
    ExhibicionDescriptionSerializer,
    ExhibicionButtonsSerializer
)

class ExhibicionViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar las exhibiciones.
    
    Este ViewSet proporciona las operaciones CRUD estándar para las exhibiciones,
    además de endpoints personalizados para gestionar sus componentes relacionados.
    
    Attributes:
        queryset: Conjunto de todas las exhibiciones.
        serializer_class: Clase serializadora para las exhibiciones.
        permission_classes: Permisos requeridos para acceder a las operaciones.
    """
    
    queryset = Exhibicion.objects.all()
    serializer_class = ExhibicionSerializer
    permission_classes = [IsAuthenticatedAndRole]
    required_role = 'admin'

    @action(detail=True, methods=['get'])
    def full_details(self, request, pk=None):
        """Obtiene todos los detalles de una exhibición específica.
        
        Este endpoint devuelve la exhibición con todas sus relaciones anidadas
        (imágenes, datos, descripciones y botones) en un solo response.
        """
        exhibicion = self.get_object()
        serializer = self.get_serializer(exhibicion)
        return Response(serializer.data)

class ExhibicionImageViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar las imágenes de exhibiciones.
    
    Este ViewSet proporciona las operaciones CRUD para las imágenes
    asociadas a las exhibiciones.
    """
    
    queryset = ExhibicionImage.objects.all()
    serializer_class = ExhibicionImageSerializer
    permission_classes = [IsAuthenticatedAndRole]
    required_role = 'admin'

    def perform_create(self, serializer):
        """Guarda la imagen y la asocia con la exhibición correspondiente."""
        serializer.save()

class ExhibicionFactsViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar los datos interesantes de exhibiciones.
    
    Este ViewSet proporciona las operaciones CRUD para los datos
    asociados a las exhibiciones.
    """
    
    queryset = ExhibicionFacts.objects.all()
    serializer_class = ExhibicionFactsSerializer
    permission_classes = [IsAuthenticatedAndRole]
    required_role = 'admin'

class ExhibicionDescriptionViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar las descripciones de exhibiciones.
    
    Este ViewSet proporciona las operaciones CRUD para las descripciones
    asociadas a las exhibiciones.
    """
    
    queryset = ExhibicionDescription.objects.all()
    serializer_class = ExhibicionDescriptionSerializer
    permission_classes = [IsAuthenticatedAndRole]
    required_role = 'admin'

class ExhibicionButtonsViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar los botones de exhibiciones.
    
    Este ViewSet proporciona las operaciones CRUD para los botones
    asociados a las exhibiciones.
    """
    
    queryset = ExhibicionButtons.objects.all()
    serializer_class = ExhibicionButtonsSerializer
    permission_classes = [IsAuthenticatedAndRole]
    required_role = 'admin'

    def perform_create(self, serializer):
        """Valida y guarda el botón con su enlace."""
        serializer.save()
