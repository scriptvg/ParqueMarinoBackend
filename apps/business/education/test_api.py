from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import timedelta
from decimal import Decimal
from unittest.mock import patch

from .models import (
    ServiciosEducativos, Instructor, Programa, Horario, Inscripcion,
    ProgramaEducativo, ProgramaItem
)
from .serializers import (
    InstructorSerializer, ProgramaSerializer, HorarioSerializer,
    InscripcionSerializer, ServiciosEducativosSerializer
)

User = get_user_model()


class InstructorSerializerTest(TestCase):
    """Test suite para InstructorSerializer."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='instructor1',
            first_name='Juan',
            last_name='Pérez'
        )
        
        self.instructor = Instructor.objects.create(
            user=self.user,
            especialidad='Biología Marina',
            experiencia_years=5,
            bio='Biólogo especializado'
        )
        
    def test_instructor_serializer_read(self):
        """Test operaciones de lectura del InstructorSerializer."""
        serializer = InstructorSerializer(self.instructor)
        data = serializer.data
        
        self.assertEqual(data['especialidad'], 'Biología Marina')
        self.assertEqual(data['experiencia_years'], 5)
        self.assertTrue(data['activo'])
        
    def test_instructor_serializer_validation(self):
        """Test validación de años de experiencia."""
        data = {
            'user': self.user.id,
            'especialidad': 'Test',
            'experiencia_years': 60,  # Demasiado alto
            'bio': 'Test bio'
        }
        
        serializer = InstructorSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('experiencia_years', serializer.errors)


class ProgramaSerializerTest(TestCase):
    """Test suite para ProgramaSerializer."""
    
    def test_programa_serializer_validation_capacidad(self):
        """Test validación de capacidades."""
        data = {
            'nombre': 'Test Programa',
            'descripcion': 'Descripción test',
            'duracion_horas': 2,
            'capacidad_min': 10,
            'capacidad_max': 5,  # Menor que mínima
            'edad_minima': 8,
            'edad_maxima': 16,
            'requisitos': '',
            'precio': '20.00'
        }
        
        serializer = ProgramaSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)
        
    def test_programa_serializer_validation_edad(self):
        """Test validación de edades."""
        data = {
            'nombre': 'Test Programa',
            'descripcion': 'Descripción test',
            'duracion_horas': 2,
            'capacidad_min': 5,
            'capacidad_max': 10,
            'edad_minima': 16,
            'edad_maxima': 8,  # Menor que mínima
            'requisitos': '',
            'precio': '20.00'
        }
        
        serializer = ProgramaSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)


class HorarioSerializerTest(TestCase):
    """Test suite para HorarioSerializer."""
    
    def setUp(self):
        self.user = User.objects.create_user(username='instructor1')
        self.instructor = Instructor.objects.create(
            user=self.user,
            especialidad='Biología',
            experiencia_years=3,
            bio='Instructor'
        )
        
        self.programa = Programa.objects.create(
            nombre='Taller Test',
            descripcion='Descripción test',
            duracion_horas=2,
            capacidad_min=5,
            capacidad_max=15,
            edad_minima=8,
            edad_maxima=14,
            requisitos='',
            precio=Decimal('20.00')
        )
        
    def test_horario_serializer_validation_fechas(self):
        """Test validación de fechas."""
        fecha_inicio = timezone.now() + timedelta(days=7)
        fecha_fin = fecha_inicio - timedelta(hours=1)  # Antes del inicio
        
        data = {
            'programa': self.programa.id,
            'instructor': self.instructor.id,
            'fecha_inicio': fecha_inicio.isoformat(),
            'fecha_fin': fecha_fin.isoformat(),
            'cupos_disponibles': 10,
            'estado': 'programado'
        }
        
        serializer = HorarioSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)
        
    def test_horario_serializer_validation_pasado(self):
        """Test validación de fechas en el pasado."""
        fecha_inicio = timezone.now() - timedelta(days=1)
        fecha_fin = fecha_inicio + timedelta(hours=2)
        
        data = {
            'programa': self.programa.id,
            'instructor': self.instructor.id,
            'fecha_inicio': fecha_inicio.isoformat(),
            'fecha_fin': fecha_fin.isoformat(),
            'cupos_disponibles': 10,
            'estado': 'programado'
        }
        
        serializer = HorarioSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)


class InscripcionSerializerTest(TestCase):
    """Test suite para InscripcionSerializer."""
    
    def setUp(self):
        self.user_instructor = User.objects.create_user(username='instructor1')
        self.user_participant = User.objects.create_user(username='participant1')
        
        self.instructor = Instructor.objects.create(
            user=self.user_instructor,
            especialidad='Biología',
            experiencia_years=3,
            bio='Instructor'
        )
        
        self.programa = Programa.objects.create(
            nombre='Taller Infantil',
            descripcion='Taller para niños',
            duracion_horas=1,
            capacidad_min=3,
            capacidad_max=10,
            edad_minima=6,
            edad_maxima=12,
            requisitos='',
            precio=Decimal('15.00')
        )
        
        fecha_inicio = timezone.now() + timedelta(days=5)
        fecha_fin = fecha_inicio + timedelta(hours=1)
        
        self.horario = Horario.objects.create(
            programa=self.programa,
            instructor=self.instructor,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
        
    def test_inscripcion_serializer_validation_edad(self):
        """Test validación de edad del participante."""
        data = {
            'horario': self.horario.id,
            'usuario': self.user_participant.id,
            'nombre_participante': 'Niño Test',
            'edad_participante': 15,  # Fuera del rango 6-12
            'estado_pago': 'pendiente'
        }
        
        serializer = InscripcionSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)
        
    def test_inscripcion_serializer_validation_cupos(self):
        """Test validación de cupos disponibles."""
        # Agotar cupos
        self.horario.cupos_disponibles = 0
        self.horario.save()
        
        data = {
            'horario': self.horario.id,
            'usuario': self.user_participant.id,
            'nombre_participante': 'Niño Test',
            'edad_participante': 8,
            'estado_pago': 'pendiente'
        }
        
        serializer = InscripcionSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)


class EducationAPITestCase(APITestCase):
    """Test suite para los endpoints de la API de Education."""
    
    def setUp(self):
        """Configurar datos de prueba y autenticación."""
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
            is_staff=True,
            is_superuser=True
        )
        
        self.regular_user = User.objects.create_user(
            username='regular',
            email='regular@example.com',
            password='regularpass123'
        )
        
        self.instructor_user = User.objects.create_user(
            username='instructor',
            email='instructor@example.com',
            password='instructorpass123'
        )
        
        self.instructor = Instructor.objects.create(
            user=self.instructor_user,
            especialidad='Biología Marina',
            experiencia_years=5,
            bio='Instructor especializado'
        )
        
        self.programa = Programa.objects.create(
            nombre='Taller de Prueba',
            descripcion='Taller para testing',
            duracion_horas=2,
            capacidad_min=5,
            capacidad_max=15,
            edad_minima=8,
            edad_maxima=16,
            requisitos='Ninguno',
            precio=Decimal('25.00')
        )
        
        self.client = APIClient()
        
    def authenticate_admin(self):
        """Autenticar como usuario admin."""
        self.client.force_authenticate(user=self.admin_user)
        
    def authenticate_regular(self):
        """Autenticar como usuario regular."""
        self.client.force_authenticate(user=self.regular_user)
        
    def authenticate_instructor(self):
        """Autenticar como instructor."""
        self.client.force_authenticate(user=self.instructor_user)
        
    def test_servicios_educativos_list_public(self):
        """Test que servicios educativos es accesible públicamente."""
        servicio = ServiciosEducativos.objects.create(
            value='test-service',
            label='Test Service',
            title='Test Educational Service'
        )
        
        url = reverse('servicios_educativos:servicios_educativos-list')
        response = self.client.get(url)
        
        # Debería ser accesible sin autenticación
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_programa_list_requires_authentication(self):
        """Test que listar programas requiere autenticación."""
        url = reverse('programas:programas-list')
        
        # Solicitud sin autenticar
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Solicitud autenticada
        self.authenticate_regular()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_instructor_list_admin_required(self):
        """Test que listar instructores requiere permisos de admin."""
        url = reverse('instructores:instructores-list')
        
        # Solicitud como usuario regular
        self.authenticate_regular()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Solicitud como admin
        self.authenticate_admin()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_inscripcion_create_authenticated(self):
        """Test creación de inscripción por usuario autenticado."""
        fecha_inicio = timezone.now() + timedelta(days=7)
        fecha_fin = fecha_inicio + timedelta(hours=2)
        
        horario = Horario.objects.create(
            programa=self.programa,
            instructor=self.instructor,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
        
        self.authenticate_regular()
        url = reverse('inscripciones:inscripciones-create')
        
        data = {
            'horario': horario.id,
            'nombre_participante': 'Juan Pérez',
            'edad_participante': 10,
            'notas': 'Sin alergias'
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar que se asignó el usuario correcto
        inscripcion = Inscripcion.objects.get(nombre_participante='Juan Pérez')
        self.assertEqual(inscripcion.usuario, self.regular_user)


class EducationBusinessLogicTest(TestCase):
    """Test suite para lógica de negocio de education."""
    
    def setUp(self):
        self.user_instructor = User.objects.create_user(username='instructor1')
        self.user_participant = User.objects.create_user(username='participant1')
        
        self.instructor = Instructor.objects.create(
            user=self.user_instructor,
            especialidad='Biología',
            experiencia_years=3,
            bio='Instructor'
        )
        
        self.programa = Programa.objects.create(
            nombre='Taller Completo',
            descripcion='Taller con capacidad limitada',
            duracion_horas=2,
            capacidad_min=2,
            capacidad_max=3,  # Capacidad muy pequeña para testing
            edad_minima=8,
            edad_maxima=12,
            requisitos='',
            precio=Decimal('20.00')
        )
        
        fecha_inicio = timezone.now() + timedelta(days=5)
        fecha_fin = fecha_inicio + timedelta(hours=2)
        
        self.horario = Horario.objects.create(
            programa=self.programa,
            instructor=self.instructor,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
        
    def test_cupos_reduction_on_inscription(self):
        """Test reducción automática de cupos al inscribirse."""
        cupos_iniciales = self.horario.cupos_disponibles
        
        inscripcion = Inscripcion.objects.create(
            horario=self.horario,
            usuario=self.user_participant,
            nombre_participante='Test Student',
            edad_participante=10
        )
        
        self.horario.refresh_from_db()
        self.assertEqual(
            self.horario.cupos_disponibles,
            cupos_iniciales - 1
        )
        
    def test_age_validation_on_inscription(self):
        """Test validación de edad al inscribirse."""
        with self.assertRaises(ValueError):
            Inscripcion.objects.create(
                horario=self.horario,
                usuario=self.user_participant,
                nombre_participante='Invalid Age Student',
                edad_participante=15  # Fuera del rango 8-12
            )
            
    def test_no_cupos_validation(self):
        """Test validación cuando no hay cupos disponibles."""
        # Agotar cupos
        self.horario.cupos_disponibles = 0
        self.horario.save()
        
        with self.assertRaises(ValueError):
            Inscripcion.objects.create(
                horario=self.horario,
                usuario=self.user_participant,
                nombre_participante='No Cupos Student',
                edad_participante=10
            )