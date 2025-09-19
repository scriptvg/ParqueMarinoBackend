from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.support.security.permissions import IsAuthenticatedAndRole
from .models import Specie, Animal, Habitat, ConservationStatus
from .serializers import (
    SpecieSerializer,
    AnimalSerializer,
    HabitatSerializer,
    ConservationStatusSerializer
)

class ConservationStatusViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar los estados de conservación.
    
    Este ViewSet proporciona las operaciones CRUD estándar para los estados
    de conservación, con restricciones de acceso según el rol del usuario.
    """
    
    queryset = ConservationStatus.objects.all()
    serializer_class = ConservationStatusSerializer
    permission_classes = [IsAuthenticatedAndRole]
    required_role = 'admin'
    http_method_names = ['get', 'post', 'put', 'delete']
    
    def destroy(self, request, *args, **kwargs):
        """Elimina un estado de conservación si no tiene especies asociadas."""
        instance = self.get_object()
        if instance.species.exists():
            return Response(
                {'detail': 'No se puede eliminar un estado que tiene especies asociadas'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def count(self, request):
        """Obtiene el número total de estados de conservación."""
        count = self.get_queryset().count()
        return Response({'count': count})

class SpecieViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar las especies.
    
    Este ViewSet proporciona operaciones CRUD para las especies, incluyendo
    endpoints adicionales para obtener información relacionada.
    """
    
    queryset = Specie.objects.all()
    serializer_class = SpecieSerializer
    permission_classes = [IsAuthenticatedAndRole]
    required_role = 'admin'
    http_method_names = ['get', 'post', 'put', 'delete']
    
    @action(detail=True, methods=['get'])
    def animals(self, request, pk=None):
        """Lista todos los animales de una especie específica."""
        specie = self.get_object()
        animals = specie.animals.all()
        serializer = AnimalSerializer(animals, many=True)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        """Elimina una especie si no tiene animales asociados."""
        instance = self.get_object()
        if instance.animals.exists():
            return Response(
                {'detail': 'No se puede eliminar una especie que tiene animales asociados'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def count(self, request):
        """Obtiene el número total de especies."""
        count = self.get_queryset().count()
        return Response({'count': count})

class AnimalViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar los animales.
    
    Este ViewSet proporciona operaciones CRUD para los animales individuales,
    con validaciones adicionales para la asignación de hábitats.
    """
    
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    permission_classes = [IsAuthenticatedAndRole]
    required_role = 'admin'
    http_method_names = ['get', 'post', 'put', 'delete']
    
    def create(self, request, *args, **kwargs):
        """Crea un nuevo animal verificando la capacidad del hábitat."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        habitat = serializer.validated_data['habitat']
        if habitat.is_full:
            return Response(
                {'detail': 'El hábitat seleccionado está lleno'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    @action(detail=False, methods=['get'])
    def count(self, request):
        """Obtiene el número total de animales."""
        count = self.get_queryset().count()
        return Response({'count': count})

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Obtiene los animales más recientes."""
        limit = int(request.GET.get('limit', 5))
        recent_animals = self.get_queryset().order_by('-id')[:limit]
        serializer = self.get_serializer(recent_animals, many=True)
        return Response(serializer.data)

class HabitatViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar los hábitats.
    
    Este ViewSet proporciona operaciones CRUD para los hábitats, incluyendo
    endpoints adicionales para obtener información sobre su ocupación.
    """
    
    queryset = Habitat.objects.all()
    serializer_class = HabitatSerializer
    permission_classes = [IsAuthenticatedAndRole]
    required_role = 'admin'
    http_method_names = ['get', 'post', 'put', 'delete']
    
    @action(detail=True, methods=['get'])
    def animals(self, request, pk=None):
        """Lista todos los animales en un hábitat específico."""
        habitat = self.get_object()
        animals = habitat.animals.all()
        serializer = AnimalSerializer(animals, many=True)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        """Elimina un hábitat si no tiene animales asociados."""
        instance = self.get_object()
        if instance.animals.exists():
            return Response(
                {'detail': 'No se puede eliminar un hábitat que tiene animales asociados'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def count(self, request):
        """Obtiene el número total de hábitats."""
        count = self.get_queryset().count()
        return Response({'count': count})
