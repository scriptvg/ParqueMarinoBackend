from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from unittest.mock import patch

from .models import (
    ServiciosEducativos, Instructor, Programa, Horario, Inscripcion,
    ProgramaEducativo, ProgramaItem
)

User = get_user_model()


class ServiciosEducativosModelTest(TestCase):
    """Test suite para el modelo ServiciosEducativos."""
    
    def test_servicios_educativos_creation(self):
        """Test creación básica de servicio educativo."""
        servicio = ServiciosEducativos.objects.create(
            value='talleres-cientificos',
            label='Talleres Científicos',
            title='Talleres de Ciencias Marinas'
        )
        
        self.assertEqual(servicio.value, 'talleres-cientificos')
        self.assertEqual(servicio.label, 'Talleres Científicos')
        self.assertEqual(str(servicio), 'talleres-cientificos')
        
    def test_servicios_educativos_unique_constraints(self):
        """Test restricciones de unicidad."""
        ServiciosEducativos.objects.create(
            value='educacion-ambiental',
            label='Educación Ambiental',
            title='Programa de Educación Ambiental'
        )
        
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                ServiciosEducativos.objects.create(
                    value='educacion-ambiental',
                    label='Otro Label',
                    title='Otro Título'
                )


class InstructorModelTest(TestCase):
    """Test suite para el modelo Instructor."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='instructor1',
            first_name='Juan',
            last_name='Pérez'
        )
        
    def test_instructor_creation(self):
        """Test creación básica de instructor."""
        instructor = Instructor.objects.create(
            user=self.user,
            especialidad='Biología Marina',
            experiencia_years=5,
            bio='Biólogo especializado en ecosistemas marinos'
        )
        
        self.assertEqual(instructor.especialidad, 'Biología Marina')
        self.assertEqual(instructor.experiencia_years, 5)
        self.assertTrue(instructor.activo)
        self.assertEqual(str(instructor), 'Juan Pérez - Biología Marina')
        
    def test_instructor_experience_validation(self):
        """Test validación de años de experiencia."""
        instructor = Instructor(
            user=self.user,
            especialidad='Test',
            experiencia_years=-1,
            bio='Test'
        )
        
        with self.assertRaises(ValidationError):
            instructor.full_clean()


class ProgramaModelTest(TestCase):
    """Test suite para el modelo Programa."""
    
    def test_programa_creation(self):
        """Test creación básica de programa."""
        programa = Programa.objects.create(
            nombre='Taller de Biología Marina',
            descripcion='Taller educativo sobre ecosistemas marinos',
            duracion_horas=3,
            capacidad_min=5,
            capacidad_max=20,
            edad_minima=8,
            edad_maxima=16,
            requisitos='Ninguno',
            precio=Decimal('25.00')
        )
        
        self.assertEqual(programa.nombre, 'Taller de Biología Marina')
        self.assertEqual(programa.precio, Decimal('25.00'))
        self.assertTrue(programa.activo)
        self.assertEqual(str(programa), 'Taller de Biología Marina')
        
    def test_programa_validation_constraints(self):
        """Test validaciones de duración y capacidades."""
        programa = Programa(
            nombre='Test',
            descripcion='Test',
            duracion_horas=0,
            capacidad_min=1,
            capacidad_max=10,
            edad_minima=5,
            edad_maxima=15,
            requisitos='',
            precio=Decimal('10.00')
        )
        
        with self.assertRaises(ValidationError):
            programa.full_clean()


class HorarioModelTest(TestCase):
    """Test suite para el modelo Horario."""
    
    def setUp(self):
        self.user = User.objects.create_user(username='instructor1')
        self.instructor = Instructor.objects.create(
            user=self.user,
            especialidad='Biología',
            experiencia_years=5,
            bio='Instructor experto'
        )
        
        self.programa = Programa.objects.create(
            nombre='Taller Marino',
            descripcion='Taller sobre vida marina',
            duracion_horas=2,
            capacidad_min=5,
            capacidad_max=15,
            edad_minima=8,
            edad_maxima=14,
            requisitos='',
            precio=Decimal('20.00')
        )
        
    def test_horario_creation(self):
        """Test creación básica de horario."""
        fecha_inicio = timezone.now() + timedelta(days=7)
        fecha_fin = fecha_inicio + timedelta(hours=2)
        
        horario = Horario.objects.create(
            programa=self.programa,
            instructor=self.instructor,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
        
        self.assertEqual(horario.programa, self.programa)
        self.assertEqual(horario.cupos_disponibles, self.programa.capacidad_max)
        self.assertEqual(horario.estado, 'programado')


class InscripcionModelTest(TestCase):
    """Test suite para el modelo Inscripcion."""
    
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
        
    def test_inscripcion_creation_valid(self):
        """Test creación válida de inscripción."""
        inscripcion = Inscripcion.objects.create(
            horario=self.horario,
            usuario=self.user_participant,
            nombre_participante='Ana García',
            edad_participante=8
        )
        
        self.assertEqual(inscripcion.nombre_participante, 'Ana García')
        self.assertEqual(inscripcion.edad_participante, 8)
        self.assertEqual(inscripcion.estado_pago, 'pendiente')
        
        # Verificar que se redujeron los cupos
        self.horario.refresh_from_db()
        self.assertEqual(self.horario.cupos_disponibles, 9)


@patch('education.models.ProgramaEducativo.image.field.storage.save')
class ProgramaEducativoModelTest(TestCase):
    """Test suite para el modelo ProgramaEducativo."""
    
    def test_programa_educativo_creation(self, mock_save):
        """Test creación básica de programa educativo."""
        mock_save.return_value = 'programas/test.jpg'
        
        programa = ProgramaEducativo.objects.create(
            title='Conservación Marina',
            description='Programa sobre conservación de especies marinas'
        )
        
        self.assertEqual(programa.title, 'Conservación Marina')
        self.assertEqual(str(programa), 'Conservación Marina')
        
    def test_programa_item_creation(self, mock_save):
        """Test creación de items de programa."""
        mock_save.return_value = 'programas/test.jpg'
        
        programa = ProgramaEducativo.objects.create(
            title='Test Programa',
            description='Descripción de prueba'
        )
        
        item = ProgramaItem.objects.create(
            programa=programa,
            text='Conocer especies marinas en peligro'
        )
        
        self.assertEqual(item.programa, programa)
        self.assertEqual(item.text, 'Conocer especies marinas en peligro')
        self.assertEqual(str(item), 'Test Programa - Conocer especies marinas en pe')
