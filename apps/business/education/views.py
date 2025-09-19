from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import (
    Instructor, Programa, Horario, Inscripcion,
    ServiciosEducativos, ServiciosEducativosImage, ServiciosEducativosFacts,
    ServiciosEducativosDescription, ServiciosEducativosButtons,
    ProgramaEducativo, ProgramaItem
)
from .serializers import (
    InstructorSerializer, ProgramaSerializer, HorarioSerializer, InscripcionSerializer,
    ServiciosEducativosSerializer, ServiciosEducativosImageSerializer,
    ServiciosEducativosFactsSerializer, ServiciosEducativosDescriptionSerializer,
    ServiciosEducativosButtonsSerializer, ProgramaEducativoSerializer, ProgramaItemSerializer
)
from apps.support.security.permissions import IsAuthenticatedAndRole

class InstructorViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar instructores
    
    Permite operaciones CRUD sobre instructores con los permisos adecuados.
    Solo los administradores pueden crear, actualizar y eliminar instructores.
    """
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer
    permission_classes = [IsAuthenticatedAndRole]
    required_role = 'admin'

    def get_queryset(self):
        """Filtra instructores activos para usuarios no admin"""
        queryset = super().get_queryset()
        if not self.request.user.groups.filter(name='admin').exists():
            queryset = queryset.filter(activo=True)
        return queryset

class ProgramaViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar programas educativos
    
    Permite operaciones CRUD sobre programas con los permisos adecuados.
    Los programas inactivos solo son visibles para administradores.
    """
    queryset = Programa.objects.all()
    serializer_class = ProgramaSerializer
    
    def get_permissions(self):
        """Define permisos según la acción"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticatedAndRole(required_role='admin')()]
        return [permissions.AllowAny()] # Allow public read

    def get_queryset(self):
        """Filtra programas activos para usuarios no admin"""
        queryset = super().get_queryset()
        if not self.request.user.groups.filter(name='admin').exists():
            queryset = queryset.filter(activo=True)
        return queryset

class HorarioViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar horarios de programas
    
    Permite operaciones CRUD sobre horarios con los permisos adecuados.
    Los instructores solo pueden ver sus propios horarios.
    """
    queryset = Horario.objects.all()
    serializer_class = HorarioSerializer
    
    def get_permissions(self):
        """Define permisos según la acción"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticatedAndRole(required_role='admin')()]
        return [permissions.AllowAny()] # Allow public read

    def get_queryset(self):
        """Filtra horarios según el rol del usuario"""
        queryset = super().get_queryset()
        user = self.request.user

        if user.groups.filter(name='instructor').exists():
            # Los instructores solo ven sus horarios
            queryset = queryset.filter(instructor__user=user)
        elif not user.groups.filter(name='admin').exists():
            # Usuarios normales solo ven horarios programados o en curso
            queryset = queryset.filter(estado__in=['programado', 'en_curso'])

        return queryset

class InscripcionViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar inscripciones
    
    Permite operaciones CRUD sobre inscripciones con los permisos adecuados.
    Los usuarios solo pueden ver y gestionar sus propias inscripciones.
    """
    queryset = Inscripcion.objects.all()
    serializer_class = InscripcionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filtra inscripciones según el rol del usuario"""
        queryset = super().get_queryset()
        user = self.request.user

        if user.groups.filter(name='admin').exists():
            return queryset
        elif user.groups.filter(name='instructor').exists():
            # Los instructores ven inscripciones de sus horarios
            return queryset.filter(horario__instructor__user=user)
        else:
            # Usuarios normales solo ven sus inscripciones
            return queryset.filter(usuario=user)

    def perform_create(self, serializer):
        """Asigna el usuario actual a la inscripción"""
        serializer.save(usuario=self.request.user)

class ServiciosEducativosViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar servicios educativos
    
    Permite operaciones CRUD sobre servicios educativos con los permisos adecuados.
    Solo los administradores pueden crear, actualizar y eliminar servicios.
    """
    queryset = ServiciosEducativos.objects.all()
    serializer_class = ServiciosEducativosSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_permissions(self):
        """Define permisos según la acción"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticatedAndRole(required_role='admin')()]
        return super().get_permissions()

class ServiciosEducativosImageViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar imágenes de servicios educativos
    
    Permite operaciones CRUD sobre imágenes de servicios con los permisos adecuados.
    Solo los administradores pueden gestionar las imágenes.
    """
    queryset = ServiciosEducativosImage.objects.all()
    serializer_class = ServiciosEducativosImageSerializer
    permission_classes = [IsAuthenticatedAndRole]
    required_role = 'admin'

class ServiciosEducativosFactsViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar datos relevantes de servicios educativos
    
    Permite operaciones CRUD sobre facts de servicios con los permisos adecuados.
    Solo los administradores pueden gestionar los facts.
    """
    queryset = ServiciosEducativosFacts.objects.all()
    serializer_class = ServiciosEducativosFactsSerializer
    permission_classes = [IsAuthenticatedAndRole]
    required_role = 'admin'

class ServiciosEducativosDescriptionViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar descripciones de servicios educativos
    
    Permite operaciones CRUD sobre descripciones de servicios con los permisos adecuados.
    Solo los administradores pueden gestionar las descripciones.
    """
    queryset = ServiciosEducativosDescription.objects.all()
    serializer_class = ServiciosEducativosDescriptionSerializer
    permission_classes = [IsAuthenticatedAndRole]
    required_role = 'admin'

class ServiciosEducativosButtonsViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar botones de servicios educativos
    
    Permite operaciones CRUD sobre botones de servicios con los permisos adecuados.
    Solo los administradores pueden gestionar los botones.
    """
    queryset = ServiciosEducativosButtons.objects.all()
    serializer_class = ServiciosEducativosButtonsSerializer
    permission_classes = [IsAuthenticatedAndRole]
    required_role = 'admin'

class ProgramaEducativoViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar programas educativos
    
    Permite operaciones CRUD sobre programas educativos con los permisos adecuados.
    Solo los administradores pueden crear, actualizar y eliminar programas.
    """
    queryset = ProgramaEducativo.objects.all()
    serializer_class = ProgramaEducativoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_permissions(self):
        """Define permisos según la acción"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticatedAndRole(required_role='admin')()]
        return super().get_permissions()

class ProgramaItemViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar items de programas educativos
    
    Permite operaciones CRUD sobre items de programas con los permisos adecuados.
    Solo los administradores pueden gestionar los items.
    """
    queryset = ProgramaItem.objects.all()
    serializer_class = ProgramaItemSerializer
    permission_classes = [IsAuthenticatedAndRole]
    required_role = 'admin'
    
    def get_queryset(self):
        """Filtra items por programa si se especifica"""
        queryset = super().get_queryset()
        programa_id = self.request.query_params.get('programa', None)
        if programa_id is not None:
            queryset = queryset.filter(programa_id=programa_id)
        return queryset
