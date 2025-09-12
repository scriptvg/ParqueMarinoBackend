from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from unittest.mock import patch, MagicMock

from apps.business.wildlife.models import ConservationStatus, Specie, Animal, Habitat
from apps.business.wildlife.serializers import (
    ConservationStatusSerializer,
    SpecieSerializer,
    AnimalSerializer,
    HabitatSerializer
)

User = get_user_model()

# ==============================
# TESTS DE SERIALIZADORES
# ==============================

class ConservationStatusSerializerTest(TestCase):
    """Pruebas unitarias para ConservationStatusSerializer"""
    
    def setUp(self):
        self.conservation_status = ConservationStatus.objects.create(name='EN')
        self.valid_data = {'name': 'VU'}
    
    def test_serializer_valid_data(self):
        """Prueba serialización con datos válidos"""
        serializer = ConservationStatusSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
    
    def test_serializer_serialization(self):
        """Prueba la serialización de una instancia"""
        serializer = ConservationStatusSerializer(self.conservation_status)
        expected_data = {
            'id': self.conservation_status.id,
            'name': 'EN'
        }
        self.assertEqual(serializer.data, expected_data)
    
    def test_serializer_invalid_choice(self):
        """Prueba serialización con opción inválida"""
        invalid_data = {'name': 'INVALID'}
        serializer = ConservationStatusSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

class SpecieSerializerTest(TestCase):
    """Pruebas unitarias para SpecieSerializer"""
    
    def setUp(self):
        self.conservation_status = ConservationStatus.objects.create(name='EN')
        self.specie = Specie.objects.create(
            name='Ballena Azul',
            scientific_name='Balaenoptera musculus',
            description='El animal más grande del mundo',
            conservation_status=self.conservation_status
        )
        self.valid_data = {
            'name': 'Orca',
            'scientific_name': 'Orcinus orca',
            'description': 'Mamífero marino depredador',
            'conservation_status_id': self.conservation_status.id
        }
    
    def test_serializer_valid_data(self):
        """Prueba serialización con datos válidos"""
        serializer = SpecieSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
    
    def test_serializer_scientific_name_validation(self):
        """Prueba validación del nombre científico"""
        invalid_data = self.valid_data.copy()
        invalid_data['scientific_name'] = 'NombreInvalido'  # Sin espacio
        
        serializer = SpecieSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('scientific_name', serializer.errors)
    
    def test_serializer_animals_count(self):
        """Prueba el campo animals_count"""
        # Crear algunos animales
        habitat = Habitat.objects.create(
            name='Test Habitat',
            capacity=10,
            description='Test'
        )
        Animal.objects.create(
            name='Animal1',
            age=5,
            specie=self.specie,
            habitat=habitat
        )
        Animal.objects.create(
            name='Animal2',
            age=3,
            specie=self.specie,
            habitat=habitat
        )
        
        serializer = SpecieSerializer(self.specie)
        self.assertEqual(serializer.data['animals_count'], 2)

class HabitatSerializerTest(TestCase):
    """Pruebas unitarias para HabitatSerializer"""
    
    def setUp(self):
        self.habitat = Habitat.objects.create(
            name='Acuario Principal',
            capacity=10,
            description='Acuario grande'
        )
        self.valid_data = {
            'name': 'Nuevo Acuario',
            'capacity': 15,
            'description': 'Descripción del nuevo acuario'
        }
    
    def test_serializer_valid_data(self):
        """Prueba serialización con datos válidos"""
        serializer = HabitatSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
    
    def test_serializer_capacity_validation(self):
        """Prueba validación de capacidad máxima"""
        invalid_data = self.valid_data.copy()
        invalid_data['capacity'] = 150  # Más de 100
        
        serializer = HabitatSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)
    
    def test_serializer_read_only_fields(self):
        """Prueba campos de solo lectura"""
        serializer = HabitatSerializer(self.habitat)
        data = serializer.data
        
        self.assertIn('current_occupancy', data)
        self.assertIn('is_full', data)
        self.assertEqual(data['current_occupancy'], 0)
        self.assertEqual(data['is_full'], False)

class AnimalSerializerTest(TestCase):
    """Pruebas unitarias para AnimalSerializer"""
    
    def setUp(self):
        self.conservation_status = ConservationStatus.objects.create(name='LC')
        self.specie = Specie.objects.create(
            name='Delfín',
            scientific_name='Delphinus delphis',
            description='Test',
            conservation_status=self.conservation_status
        )
        self.habitat = Habitat.objects.create(
            name='Piscina',
            capacity=5,
            description='Test'
        )
        self.valid_data = {
            'name': 'Flipper',
            'age': 7,
            'specie_id': self.specie.id,
            'habitat_id': self.habitat.id
        }
    
    def test_serializer_valid_data(self):
        """Prueba serialización con datos válidos"""
        serializer = AnimalSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
    
    def test_serializer_age_validation(self):
        """Prueba validación de edad"""
        invalid_data = self.valid_data.copy()
        invalid_data['age'] = 150  # Edad muy alta
        
        serializer = AnimalSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('age', serializer.errors)
    
    def test_serializer_full_habitat_validation(self):
        """Prueba validación de hábitat lleno"""
        # Llenar el hábitat
        small_habitat = Habitat.objects.create(
            name='Pequeño',
            capacity=1,
            description='Test'
        )
        Animal.objects.create(
            name='Existing',
            age=5,
            specie=self.specie,
            habitat=small_habitat
        )
        
        invalid_data = self.valid_data.copy()
        invalid_data['habitat_id'] = small_habitat.id
        
        serializer = AnimalSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)

# ====================
# TESTS DE VISTAS
# ====================

class WildlifeAPITestCase(APITestCase):
    """Clase base para tests de API"""
    
    def setUp(self):
        # Crear usuario admin
        self.user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
            is_staff=True,
            is_superuser=True
        )
        
        # Crear grupo admin y asignar al usuario
        from django.contrib.auth.models import Group
        admin_group, created = Group.objects.get_or_create(name='admin')
        self.user.groups.add(admin_group)
        
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # Crear datos base
        self.conservation_status = ConservationStatus.objects.create(name='EN')
        self.specie = Specie.objects.create(
            name='Ballena Azul',
            scientific_name='Balaenoptera musculus',
            description='Test',
            conservation_status=self.conservation_status
        )
        self.habitat = Habitat.objects.create(
            name='Acuario Principal',
            capacity=10,
            description='Test'
        )
        self.animal = Animal.objects.create(
            name='Flipper',
            age=5,
            specie=self.specie,
            habitat=self.habitat
        )

class ConservationStatusViewSetTest(WildlifeAPITestCase):
    """Pruebas para ConservationStatusViewSet"""
    
    def test_list_conservation_statuses(self):
        """Prueba listar estados de conservación"""
        url = '/api/wildlife/conservation-status/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_conservation_status(self):
        """Prueba crear estado de conservación"""
        url = '/api/wildlife/conservation-status/create/'
        data = {'name': 'VU'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ConservationStatus.objects.filter(name='VU').exists())
    
    def test_delete_conservation_status_with_species(self):
        """Prueba que no se pueda eliminar estado con especies"""
        url = f'/api/wildlife/conservation-status/{self.conservation_status.id}/delete/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', response.data)

class SpecieViewSetTest(WildlifeAPITestCase):
    """Pruebas para SpecieViewSet"""
    
    def test_list_species(self):
        """Prueba listar especies"""
        url = '/api/wildlife/species/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_specie(self):
        """Prueba crear especie"""
        url = '/api/wildlife/species/create/'
        data = {
            'name': 'Orca',
            'scientific_name': 'Orcinus orca',
            'description': 'Mamífero marino',
            'conservation_status_id': self.conservation_status.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Specie.objects.filter(name='Orca').exists())
    
    def test_specie_animals_endpoint(self):
        """Prueba endpoint personalizado de animales de especie"""
        url = f'/api/wildlife/species/{self.specie.id}/animals/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Flipper')
    
    def test_delete_specie_with_animals(self):
        """Prueba que no se pueda eliminar especie con animales"""
        url = f'/api/wildlife/species/{self.specie.id}/delete/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', response.data)

class HabitatViewSetTest(WildlifeAPITestCase):
    """Pruebas para HabitatViewSet"""
    
    def test_list_habitats(self):
        """Prueba listar hábitats"""
        url = '/api/wildlife/habitats/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_habitat(self):
        """Prueba crear hábitat"""
        url = '/api/wildlife/habitats/create/'
        data = {
            'name': 'Nuevo Acuario',
            'capacity': 15,
            'description': 'Acuario nuevo para pruebas'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Habitat.objects.filter(name='Nuevo Acuario').exists())
    
    def test_habitat_animals_endpoint(self):
        """Prueba endpoint personalizado de animales de hábitat"""
        url = f'/api/wildlife/habitats/{self.habitat.id}/animals/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Flipper')
    
    def test_delete_habitat_with_animals(self):
        """Prueba que no se pueda eliminar hábitat con animales"""
        url = f'/api/wildlife/habitats/{self.habitat.id}/delete/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', response.data)

class AnimalViewSetTest(WildlifeAPITestCase):
    """Pruebas para AnimalViewSet"""
    
    def test_list_animals(self):
        """Prueba listar animales"""
        url = '/api/wildlife/animals/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_animal(self):
        """Prueba crear animal"""
        url = '/api/wildlife/animals/create/'
        data = {
            'name': 'Splash',
            'age': 3,
            'specie_id': self.specie.id,
            'habitat_id': self.habitat.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Animal.objects.filter(name='Splash').exists())
    
    def test_create_animal_full_habitat(self):
        """Prueba crear animal en hábitat lleno"""
        # Crear hábitat pequeño y llenarlo
        small_habitat = Habitat.objects.create(
            name='Pequeño',
            capacity=1,
            description='Test'
        )
        Animal.objects.create(
            name='Existing',
            age=5,
            specie=self.specie,
            habitat=small_habitat
        )
        
        url = '/api/wildlife/animals/create/'
        data = {
            'name': 'NewAnimal',
            'age': 2,
            'specie_id': self.specie.id,
            'habitat_id': small_habitat.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', response.data)

# ===========================================
# TESTS DE SIGNALS (S3 DELETION)
# ===========================================

class WildlifeSignalsTest(TestCase):
    """Pruebas para las señales de eliminación S3"""
    
    def setUp(self):
        self.conservation_status = ConservationStatus.objects.create(name='LC')
        
    @patch('utils.s3_utils.delete_s3_files_from_instance')
    def test_specie_deletion_triggers_s3_cleanup(self, mock_delete_s3):
        """Prueba que eliminar una especie active la señal de S3"""
        specie = Specie.objects.create(
            name='Test Specie',
            scientific_name='Testus speciei',
            description='Test description',
            conservation_status=self.conservation_status
        )
        
        # Simular que la señal se ejecuta
        mock_delete_s3.return_value = {'deleted': 1, 'errors': 0, 'files': []}
        
        specie.delete()
        
        # Verificar que se llamó la función de eliminación S3
        mock_delete_s3.assert_called_once()
    
    @patch('utils.s3_utils.delete_old_s3_file')
    def test_specie_image_update_triggers_s3_cleanup(self, mock_delete_old):
        """Prueba que actualizar imagen de especie active la señal de S3"""
        specie = Specie.objects.create(
            name='Test Specie',
            scientific_name='Testus speciei',
            description='Test description',
            conservation_status=self.conservation_status
        )
        
        # Simular actualización de imagen
        mock_delete_old.return_value = True
        
        # Actualizar la especie (simular cambio de imagen)
        specie.description = 'Updated description'
        specie.save()
        
        # Verificar que se llamó la función de eliminación de archivo anterior
        mock_delete_old.assert_called_once()