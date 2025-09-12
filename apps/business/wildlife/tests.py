from django.test import TestCase, TransactionTestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from unittest.mock import patch, MagicMock
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import ConservationStatus, Specie, Animal, Habitat
from .serializers import (
    ConservationStatusSerializer,
    SpecieSerializer,
    AnimalSerializer,
    HabitatSerializer
)

User = get_user_model()

# =====================
# TESTS DE MODELOS
# =====================

class ConservationStatusModelTest(TestCase):
    """Pruebas unitarias para el modelo ConservationStatus"""
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.status_data = {
            'name': 'EN'  # Endangered
        }
    
    def test_conservation_status_creation(self):
        """Prueba la creación de un estado de conservación"""
        status = ConservationStatus.objects.create(**self.status_data)
        self.assertEqual(status.name, 'EN')
        self.assertEqual(str(status), 'Endangered')
        self.assertIsNotNone(status.id)
    
    def test_conservation_status_unique_constraint(self):
        """Prueba que no se puedan crear estados duplicados"""
        ConservationStatus.objects.create(**self.status_data)
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                ConservationStatus.objects.create(**self.status_data)
    
    def test_conservation_status_str_representation(self):
        """Prueba la representación string del modelo"""
        status = ConservationStatus.objects.create(name='CR')
        self.assertEqual(str(status), 'Critically Endangered')
    
    def test_conservation_status_choices(self):
        """Prueba que solo se acepten valores válidos"""
        valid_choices = ['LC', 'NT', 'VU', 'EN', 'CR', 'EW', 'EX']
        for choice in valid_choices:
            status = ConservationStatus(name=choice)
            # No debe lanzar excepción
            status.full_clean()
    
    def test_conservation_status_ordering(self):
        """Prueba el ordenamiento por defecto"""
        ConservationStatus.objects.create(name='VU')
        ConservationStatus.objects.create(name='EN')
        ConservationStatus.objects.create(name='CR')
        
        statuses = list(ConservationStatus.objects.all())
        names = [s.name for s in statuses]
        self.assertEqual(names, ['CR', 'EN', 'VU'])

class SpecieModelTest(TestCase):
    """Pruebas unitarias para el modelo Specie"""
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.conservation_status = ConservationStatus.objects.create(name='EN')
        self.specie_data = {
            'name': 'Ballena Azul',
            'scientific_name': 'Balaenoptera musculus',
            'description': 'La ballena azul es el animal más grande del mundo.',
            'conservation_status': self.conservation_status
        }
    
    def test_specie_creation(self):
        """Prueba la creación de una especie"""
        specie = Specie.objects.create(**self.specie_data)
        self.assertEqual(specie.name, 'Ballena Azul')
        self.assertEqual(specie.scientific_name, 'Balaenoptera musculus')
        self.assertEqual(specie.conservation_status, self.conservation_status)
        self.assertIsNotNone(specie.id)
    
    def test_specie_str_representation(self):
        """Prueba la representación string del modelo"""
        specie = Specie.objects.create(**self.specie_data)
        expected = 'Ballena Azul (Balaenoptera musculus)'
        self.assertEqual(str(specie), expected)
    
    def test_specie_unique_constraints(self):
        """Prueba que name y scientific_name sean únicos"""
        Specie.objects.create(**self.specie_data)
        
        # Probar duplicado de name
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                Specie.objects.create(
                    name='Ballena Azul',
                    scientific_name='Otro nombre',
                    description='Otra descripción',
                    conservation_status=self.conservation_status
                )
        
        # Probar duplicado de scientific_name
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                Specie.objects.create(
                    name='Otro nombre',
                    scientific_name='Balaenoptera musculus',
                    description='Otra descripción',
                    conservation_status=self.conservation_status
                )
    
    def test_specie_get_image_url_with_image(self):
        """Prueba get_image_url cuando hay imagen"""
        specie = Specie.objects.create(**self.specie_data)
        
        # Mock de imagen
        mock_image = MagicMock()
        mock_image.url = 'http://example.com/image.jpg'
        specie.image = mock_image
        
        self.assertEqual(specie.get_image_url(), 'http://example.com/image.jpg')
    
    def test_specie_get_image_url_without_image(self):
        """Prueba get_image_url cuando no hay imagen"""
        specie = Specie.objects.create(**self.specie_data)
        self.assertIsNone(specie.get_image_url())
    
    def test_specie_ordering(self):
        """Prueba el ordenamiento por nombre"""
        Specie.objects.create(
            name='Zebra',
            scientific_name='Equus zebra',
            description='Test',
            conservation_status=self.conservation_status
        )
        Specie.objects.create(**self.specie_data)
        
        species = list(Specie.objects.all())
        names = [s.name for s in species]
        self.assertEqual(names, ['Ballena Azul', 'Zebra'])

class HabitatModelTest(TestCase):
    """Pruebas unitarias para el modelo Habitat"""
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.habitat_data = {
            'name': 'Acuario Principal',
            'capacity': 10,
            'description': 'Acuario grande para mamíferos marinos'
        }
    
    def test_habitat_creation(self):
        """Prueba la creación de un hábitat"""
        habitat = Habitat.objects.create(**self.habitat_data)
        self.assertEqual(habitat.name, 'Acuario Principal')
        self.assertEqual(habitat.capacity, 10)
        self.assertIsNotNone(habitat.id)
    
    def test_habitat_str_representation(self):
        """Prueba la representación string del modelo"""
        habitat = Habitat.objects.create(**self.habitat_data)
        self.assertEqual(str(habitat), 'Acuario Principal')
    
    def test_habitat_unique_name(self):
        """Prueba que el nombre del hábitat sea único"""
        Habitat.objects.create(**self.habitat_data)
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                Habitat.objects.create(**self.habitat_data)
    
    def test_habitat_current_occupancy_empty(self):
        """Prueba la propiedad current_occupancy cuando está vacío"""
        habitat = Habitat.objects.create(**self.habitat_data)
        self.assertEqual(habitat.current_occupancy, 0)
    
    def test_habitat_current_occupancy_with_animals(self):
        """Prueba la propiedad current_occupancy con animales"""
        habitat = Habitat.objects.create(**self.habitat_data)
        conservation_status = ConservationStatus.objects.create(name='LC')
        specie = Specie.objects.create(
            name='Delfín',
            scientific_name='Delphinus delphis',
            description='Test',
            conservation_status=conservation_status
        )
        
        # Crear algunos animales
        Animal.objects.create(name='Flipper', age=5, specie=specie, habitat=habitat)
        Animal.objects.create(name='Splash', age=3, specie=specie, habitat=habitat)
        
        self.assertEqual(habitat.current_occupancy, 2)
    
    def test_habitat_is_full_property(self):
        """Prueba la propiedad is_full"""
        habitat = Habitat.objects.create(
            name='Pequeño Acuario',
            capacity=2,
            description='Acuario pequeño'
        )
        conservation_status = ConservationStatus.objects.create(name='LC')
        specie = Specie.objects.create(
            name='Pez',
            scientific_name='Pisces test',
            description='Test',
            conservation_status=conservation_status
        )
        
        # Hábitat vacío no está lleno
        self.assertFalse(habitat.is_full)
        
        # Agregar un animal
        Animal.objects.create(name='Pez1', age=1, specie=specie, habitat=habitat)
        self.assertFalse(habitat.is_full)
        
        # Agregar segundo animal (lleno)
        Animal.objects.create(name='Pez2', age=1, specie=specie, habitat=habitat)
        self.assertTrue(habitat.is_full)
        
        # Agregar tercer animal (sobre capacidad)
        Animal.objects.create(name='Pez3', age=1, specie=specie, habitat=habitat)
        self.assertTrue(habitat.is_full)

class AnimalModelTest(TestCase):
    """Pruebas unitarias para el modelo Animal"""
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.conservation_status = ConservationStatus.objects.create(name='LC')
        self.specie = Specie.objects.create(
            name='Delfín',
            scientific_name='Delphinus delphis',
            description='Mamífero marino inteligente',
            conservation_status=self.conservation_status
        )
        self.habitat = Habitat.objects.create(
            name='Piscina de Delfines',
            capacity=5,
            description='Hábitat para delfines'
        )
        self.animal_data = {
            'name': 'Flipper',
            'age': 7,
            'specie': self.specie,
            'habitat': self.habitat
        }
    
    def test_animal_creation(self):
        """Prueba la creación de un animal"""
        animal = Animal.objects.create(**self.animal_data)
        self.assertEqual(animal.name, 'Flipper')
        self.assertEqual(animal.age, 7)
        self.assertEqual(animal.specie, self.specie)
        self.assertEqual(animal.habitat, self.habitat)
        self.assertIsNotNone(animal.id)
    
    def test_animal_str_representation(self):
        """Prueba la representación string del modelo"""
        animal = Animal.objects.create(**self.animal_data)
        expected = 'Flipper - Delfín'
        self.assertEqual(str(animal), expected)
    
    def test_animal_relationships(self):
        """Prueba las relaciones del modelo Animal"""
        animal = Animal.objects.create(**self.animal_data)
        
        # Verificar relación con especie
        self.assertIn(animal, self.specie.animals.all())
        
        # Verificar relación con hábitat
        self.assertIn(animal, self.habitat.animals.all())
    
    def test_animal_ordering(self):
        """Prueba el ordenamiento por nombre"""
        Animal.objects.create(
            name='Zebra',
            age=5,
            specie=self.specie,
            habitat=self.habitat
        )
        Animal.objects.create(**self.animal_data)
        
        animals = list(Animal.objects.all())
        names = [a.name for a in animals]
        self.assertEqual(names, ['Flipper', 'Zebra'])
