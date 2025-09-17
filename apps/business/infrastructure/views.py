from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from apps.support.security.permissions import IsAuthenticatedAndRole
from .serializers import SectionsSerializer

class InfrastructureListAPIView(APIView):
    """Vista para obtener un resumen general de la infraestructura del zoológico.

    Proporciona información consolidada sobre las secciones y hábitats,
    incluyendo estadísticas y métricas relevantes.

    Endpoint:
        GET /infrastructure/summary/

    Respuesta:
        - total_sections: Número total de secciones
        - total_habitats: Número total de hábitats
        - total_animals: Suma total de animales en todos los hábitats
        - sections_summary: Lista de secciones con sus hábitats asociados
        - empty_sections: Secciones sin hábitats asignados
        - full_sections: Secciones con más hábitats
    """
    permission_classes = [IsAuthenticatedAndRole]
    
    def get(self, request):
        try:
            # Import models inside method
            from .models import Sections
            from apps.business.wildlife.models import Habitat
            
            # Obtener todas las secciones y hábitats
            sections = Sections.objects.all()
            habitats = Habitat.objects.all()

            # Calcular estadísticas
            total_sections = sections.count()
            total_habitats = habitats.count()
            total_animals = sum(habitat.capacity for habitat in habitats)  # Changed from nums_animals to capacity

            # Preparar resumen de secciones
            sections_summary = [{
                'id': section.id,
                'name': section.name,
                'num_habitats': section.num_habitats,
                'total_animals': sum(h.capacity for h in section.habitats.all()),  # Changed from nums_animals to capacity
                'habitats': [{
                    'id': h.id,
                    'name': h.name,
                    'nums_animals': h.capacity  # Changed from nums_animals to capacity
                } for h in section.habitats.all()]
            } for section in sections]

            # Identificar secciones vacías y llenas
            empty_sections = [{
                'id': section.id,
                'name': section.name
            } for section in sections if section.num_habitats == 0]

            full_sections = sorted(
                [s for s in sections_summary if s['num_habitats'] > 0],
                key=lambda x: x['num_habitats'],
                reverse=True
            )[:3]

            return Response({
                'total_sections': total_sections,
                'total_habitats': total_habitats,
                'total_animals': total_animals,
                'sections_summary': sections_summary,
                'empty_sections': empty_sections,
                'full_sections': full_sections
            })

        except Exception as e:
            return Response(
                {"error": f"Error al obtener el resumen de infraestructura: {str(e)}"},
                status=500
            )


class HabitatViewSet(viewsets.ModelViewSet):  # Renamed from Habitats_ViewSet
    """ViewSet para gestionar los hábitats del zoológico.

    Este ViewSet proporciona operaciones CRUD para los hábitats, que son los espacios
    específicos donde viven los animales dentro de cada sección del zoológico.

    Endpoints:
        - GET /habitats/: Lista todos los hábitats
        - POST /habitats/: Crea un nuevo hábitat
        - GET /habitats/{id}/: Obtiene los detalles de un hábitat específico
        - PUT /habitats/{id}/: Actualiza un hábitat existente
        - DELETE /habitats/{id}/: Elimina un hábitat

    Permisos:
        - Se requiere autenticación para todas las operaciones
        - Solo usuarios con rol 'admin' pueden crear, actualizar o eliminar
        - Cualquier usuario autenticado puede ver los hábitats
    """
    
    permission_classes = [IsAuthenticatedAndRole]
    http_method_names = ['get', 'post', 'put', 'delete']
    required_role = 'admin'

    def get_queryset(self):
        # Import model inside method
        from apps.business.wildlife.models import Habitat
        return Habitat.objects.all()
    
    def get_serializer_class(self):
        # Import serializer inside method
        from .serializers import HabitatSerializer
        return HabitatSerializer

    def perform_create(self, serializer):
        """Crea un nuevo hábitat verificando permisos y validando datos."""
        try:
            # Import models inside method
            from .models import Sections
            
            # Verificar que la sección existe
            section_id = self.request.data.get('section')
            if section_id and not Sections.objects.filter(id=section_id).exists():
                raise serializers.ValidationError("La sección especificada no existe")
            
            serializer.save()
        except Exception as e:
            raise serializers.ValidationError(f"Error al crear el hábitat: {str(e)}")

    def perform_update(self, serializer):
        """Actualiza un hábitat existente verificando permisos y validando datos."""
        try:
            # Import models inside method
            from .models import Sections
            
            # Verificar que la sección existe si se está actualizando
            section_id = self.request.data.get('section')
            if section_id and not Sections.objects.filter(id=section_id).exists():
                raise serializers.ValidationError("La sección especificada no existe")
            
            serializer.save()
        except Exception as e:
            raise serializers.ValidationError(f"Error al actualizar el hábitat: {str(e)}")

    def perform_destroy(self, instance):
        """Elimina un hábitat verificando que no tenga animales asociados."""
        # Import model inside method
        from apps.business.wildlife.models import Animal
        
        if instance.animals.count() > 0:
            raise serializers.ValidationError(
                "No se puede eliminar el hábitat porque tiene animales asociados"
            )
        try:
            instance.delete()
        except Exception as e:
            raise serializers.ValidationError(f"Error al eliminar el hábitat: {str(e)}")

class SectionsViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar las secciones del zoológico.

    Este ViewSet proporciona operaciones CRUD para las secciones, que son áreas específicas
    del zoológico donde se agrupan diferentes hábitats y animales.

    Endpoints:
        - GET /sections/: Lista todas las secciones
        - POST /sections/: Crea una nueva sección
        - GET /sections/{id}/: Obtiene los detalles de una sección específica
        - PUT /sections/{id}/: Actualiza una sección existente
        - DELETE /sections/{id}/: Elimina una sección

    Permisos:
        - Se requiere autenticación para todas las operaciones
        - Solo usuarios con rol 'admin' o 'manager' pueden crear, actualizar o eliminar
        - Cualquier usuario autenticado puede ver las secciones
    """
    
    permission_classes = [IsAuthenticatedAndRole]
    http_method_names = ['get', 'post', 'put', 'delete']
    required_role = ['admin', 'manager']

    def get_queryset(self):
        # Import model inside method
        from .models import Sections
        return Sections.objects.all()
        
    def get_serializer_class(self):
        return SectionsSerializer

    def perform_create(self, serializer):
        """Crea una nueva sección verificando permisos y validando datos."""
        try:
            serializer.save()
        except Exception as e:
            raise serializers.ValidationError(f"Error al crear la sección: {str(e)}")

    def perform_update(self, serializer):
        """Actualiza una sección existente verificando permisos y validando datos."""
        try:
            serializer.save()
        except Exception as e:
            raise serializers.ValidationError(f"Error al actualizar la sección: {str(e)}")

    def perform_destroy(self, instance):
        """Elimina una sección verificando que no tenga hábitats asociados."""
        if instance.num_habitats > 0:
            raise serializers.ValidationError(
                "No se puede eliminar la sección porque tiene hábitats asociados"
            )
        try:
            instance.delete()
        except Exception as e:
            raise serializers.ValidationError(f"Error al eliminar la sección: {str(e)}")