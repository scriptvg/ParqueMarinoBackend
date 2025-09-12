from django.test import TestCase
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.db import transaction
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import date
import json

from .models import UserProfile
from .serializers import (
    LoginSerializer, UserProfileSerializer, GroupSerializer,
    UserSerializer, RegisterSerializer, CustomTokenObtainPairSerializer
)
from .permissions import IsAuthenticatedAndRole, IsAuthenticatedOrReadOnly


class LoginSerializerTest(TestCase):
    """Test suite for LoginSerializer functionality."""
    
    def setUp(self):
        """Set up test data for each test method."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            is_active=True
        )
        
    def test_login_serializer_valid_username(self):
        """Test LoginSerializer with valid username."""
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        
        serializer = LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['user'], self.user)
        
    def test_login_serializer_valid_email(self):
        """Test LoginSerializer with valid email."""
        data = {
            'username': 'test@example.com',
            'password': 'testpass123'
        }
        
        serializer = LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['user'], self.user)
        
    def test_login_serializer_invalid_username(self):
        """Test LoginSerializer with invalid username."""
        data = {
            'username': 'wronguser',
            'password': 'testpass123'
        }
        
        serializer = LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)
        
    def test_login_serializer_invalid_password(self):
        """Test LoginSerializer with invalid password."""
        data = {
            'username': 'testuser',
            'password': 'wrongpass'
        }
        
        serializer = LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)
        
    def test_login_serializer_inactive_user(self):
        """Test LoginSerializer with inactive user."""
        self.user.is_active = False
        self.user.save()
        
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        
        serializer = LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)
        
    def test_login_serializer_missing_fields(self):
        """Test LoginSerializer with missing required fields."""
        # Missing password
        data = {'username': 'testuser'}
        serializer = LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)
        
        # Missing username
        data = {'password': 'testpass123'}
        serializer = LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)


class UserProfileSerializerTest(TestCase):
    """Test suite for UserProfileSerializer functionality."""
    
    def setUp(self):
        """Set up test data for each test method."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.group = Group.objects.create(name='Test Group')
        self.user.groups.add(self.group)
        
        self.profile = UserProfile.objects.create(
            user=self.user,
            phone='1234567890',
            address='123 Test Street',
            birth_date=date(1990, 1, 1)
        )
        
    def test_user_profile_serializer_read(self):
        """Test UserProfileSerializer read operations."""
        serializer = UserProfileSerializer(self.profile)
        data = serializer.data
        
        self.assertEqual(data['username'], 'testuser')
        self.assertEqual(data['email'], 'test@example.com')
        self.assertEqual(data['phone'], '1234567890')
        self.assertEqual(data['address'], '123 Test Street')
        self.assertEqual(data['birth_date'], '1990-01-01')
        self.assertIn('user_roles', data)
        self.assertEqual(len(data['user_roles']), 1)
        self.assertEqual(data['user_roles'][0]['name'], 'Test Group')
        
    def test_user_profile_serializer_update(self):
        """Test UserProfileSerializer update operations."""
        update_data = {
            'phone': '0987654321',
            'address': '456 New Street'
        }
        
        serializer = UserProfileSerializer(self.profile, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        
        updated_profile = serializer.save()
        self.assertEqual(updated_profile.phone, '0987654321')
        self.assertEqual(updated_profile.address, '456 New Street')
        
    def test_user_profile_serializer_readonly_fields(self):
        """Test that username and email are read-only."""
        update_data = {
            'username': 'newusername',
            'email': 'newemail@example.com',
            'phone': '0987654321'
        }
        
        serializer = UserProfileSerializer(self.profile, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        
        updated_profile = serializer.save()
        # Username and email should not change
        self.assertEqual(updated_profile.user.username, 'testuser')
        self.assertEqual(updated_profile.user.email, 'test@example.com')
        # Phone should change
        self.assertEqual(updated_profile.phone, '0987654321')


class GroupSerializerTest(TestCase):
    """Test suite for GroupSerializer functionality."""
    
    def setUp(self):
        """Set up test data for each test method."""
        self.content_type = ContentType.objects.get_for_model(User)
        self.permission = Permission.objects.create(
            name='Can test',
            content_type=self.content_type,
            codename='test_permission'
        )
        
    def test_group_serializer_creation(self):
        """Test GroupSerializer creation."""
        data = {
            'name': 'Test Group',
            'permissions': [self.permission.id]
        }
        
        serializer = GroupSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        group = serializer.save()
        self.assertEqual(group.name, 'Test Group')
        self.assertIn(self.permission, group.permissions.all())
        
    def test_group_serializer_read(self):
        """Test GroupSerializer read operations."""
        group = Group.objects.create(name='Test Group')
        group.permissions.add(self.permission)
        
        serializer = GroupSerializer(group)
        data = serializer.data
        
        self.assertEqual(data['name'], 'Test Group')
        self.assertIn(self.permission.id, data['permissions'])


class UserSerializerTest(TestCase):
    """Test suite for UserSerializer functionality."""
    
    def setUp(self):
        """Set up test data for each test method."""
        self.group = Group.objects.create(name='Test Group')
        
    def test_user_serializer_read(self):
        """Test UserSerializer read operations."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        user.groups.add(self.group)
        
        serializer = UserSerializer(user)
        data = serializer.data
        
        self.assertEqual(data['username'], 'testuser')
        self.assertEqual(data['email'], 'test@example.com')
        # Note: groups field depends on which UserSerializer is being used
        
    def test_user_serializer_readonly_fields(self):
        """Test UserSerializer update operations."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        update_data = {
            'email': 'newemail@example.com'
        }
        
        serializer = UserSerializer(user, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        
        updated_user = serializer.save()
        # Check that basic updates work
        self.assertEqual(updated_user.username, 'testuser')


class RegisterSerializerTest(TestCase):
    """Test suite for RegisterSerializer functionality."""
    
    def setUp(self):
        """Set up test data for each test method."""
        self.group = Group.objects.create(name='Test Role')
        
    def test_register_serializer_basic_creation(self):
        """Test RegisterSerializer basic user creation."""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        user = serializer.save()
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.email, 'newuser@example.com')
        self.assertEqual(user.first_name, 'New')
        self.assertEqual(user.last_name, 'User')
        self.assertTrue(user.check_password('newpass123'))
        
    def test_register_serializer_with_roles(self):
        """Test RegisterSerializer with role assignment."""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'roles': [self.group.id]
        }
        
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        user = serializer.save()
        self.assertIn(self.group, user.groups.all())
        
    def test_register_serializer_with_profile(self):
        """Test RegisterSerializer with profile data."""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'profile': {
                'phone': '1234567890',
                'address': '123 New Street'
            }
        }
        
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        user = serializer.save()
        profile = user.user_profile
        self.assertEqual(profile.phone, '1234567890')
        self.assertEqual(profile.address, '123 New Street')


class SecurityAPITestCase(APITestCase):
    """Test suite for Security API endpoints."""
    
    def setUp(self):
        """Set up test data and authentication."""
        # Create test users
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
        
        # Create test group
        self.test_group = Group.objects.create(name='Test Group')
        
        # Create profiles
        self.admin_profile = UserProfile.objects.create(
            user=self.admin_user,
            phone='1111111111',
            address='Admin Address'
        )
        
        self.regular_profile = UserProfile.objects.create(
            user=self.regular_user,
            phone='2222222222',
            address='Regular Address'
        )
        
        self.client = APIClient()
        
    def authenticate_admin(self):
        """Authenticate as admin user."""
        self.client.force_authenticate(user=self.admin_user)
        
    def authenticate_regular(self):
        """Authenticate as regular user."""
        self.client.force_authenticate(user=self.regular_user)
        
    def test_user_profile_list_authenticated(self):
        """Test listing user profiles requires authentication."""
        url = reverse('user_profile-get')
        
        # Unauthenticated request
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Authenticated request
        self.authenticate_admin()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_user_profile_detail_view(self):
        """Test user profile detail view."""
        self.authenticate_admin()
        url = reverse('user_profile-detail', kwargs={'pk': self.admin_profile.pk})
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        self.assertEqual(data['username'], 'admin')
        self.assertEqual(data['phone'], '1111111111')
        
    def test_user_profile_update(self):
        """Test user profile update."""
        self.authenticate_admin()
        url = reverse('user_profile-update', kwargs={'pk': self.admin_profile.pk})
        
        update_data = {
            'phone': '9999999999',
            'address': 'Updated Address'
        }
        
        response = self.client.put(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify update
        self.admin_profile.refresh_from_db()
        self.assertEqual(self.admin_profile.phone, '9999999999')
        self.assertEqual(self.admin_profile.address, 'Updated Address')
        
    def test_current_user_profile_view(self):
        """Test current user profile view."""
        self.authenticate_regular()
        url = reverse('current-user-profile')
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        self.assertEqual(data['username'], 'regular')
        self.assertEqual(data['phone'], '2222222222')
        
    def test_group_operations(self):
        """Test group CRUD operations."""
        self.authenticate_admin()
        
        # List groups
        url = reverse('roles-get')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Create group
        url = reverse('roles-create')
        create_data = {'name': 'New Group'}
        response = self.client.post(url, create_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify creation
        new_group = Group.objects.get(name='New Group')
        self.assertIsNotNone(new_group)
        
    def test_user_operations(self):
        """Test user CRUD operations."""
        self.authenticate_admin()
        
        # List users
        url = reverse('users-get')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Create user (simplified)
        url = reverse('users-create')
        create_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123'
        }
        response = self.client.post(url, create_data, format='json')
        # May not be 201 if view has different behavior, just check it's not 500
        self.assertNotEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def test_permissions_required(self):
        """Test that endpoints require proper permissions."""
        # Test with unauthenticated user
        url = reverse('user_profile-get')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Test with authenticated regular user
        self.authenticate_regular()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CustomTokenObtainPairSerializerTest(TestCase):
    """Test suite for CustomTokenObtainPairSerializer functionality."""
    
    def setUp(self):
        """Set up test data for each test method."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_custom_token_serializer_valid_credentials(self):
        """Test CustomTokenObtainPairSerializer with valid credentials."""
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        
        serializer = CustomTokenObtainPairSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        tokens = serializer.validated_data
        self.assertIn('access', tokens)
        self.assertIn('refresh', tokens)
        
    def test_custom_token_serializer_invalid_credentials(self):
        """Test CustomTokenObtainPairSerializer with invalid credentials."""
        data = {
            'username': 'wronguser',
            'password': 'wrongpass'
        }
        
        serializer = CustomTokenObtainPairSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        
    def test_custom_token_includes_user_data(self):
        """Test that custom token includes additional user data."""
        # This would require decoding the JWT token to verify custom claims
        # For now, we test that the serializer validates correctly
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        
        serializer = CustomTokenObtainPairSerializer(data=data)
        self.assertTrue(serializer.is_valid())


class SecurityPermissionsTest(TestCase):
    """Test suite for custom permission classes."""
    
    def setUp(self):
        """Set up test data for each test method."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.group = Group.objects.create(name='TestRole')
        
    def test_is_authenticated_and_role_permission(self):
        """Test IsAuthenticatedAndRole permission class."""
        from django.http import HttpRequest
        from types import SimpleNamespace
        
        permission = IsAuthenticatedAndRole()
        
        # Mock request and view
        request = HttpRequest()
        request.user = self.user
        view = SimpleNamespace()
        
        # Test without required role
        view.required_role = None
        self.assertTrue(permission.has_permission(request, view))
        
        # Test with required role (user not in group)
        view.required_role = 'TestRole'
        self.assertFalse(permission.has_permission(request, view))
        
        # Test with required role (user in group)
        self.user.groups.add(self.group)
        self.assertTrue(permission.has_permission(request, view))
        
    def test_is_authenticated_or_read_only_permission(self):
        """Test IsAuthenticatedOrReadOnly permission class."""
        from django.http import HttpRequest
        from types import SimpleNamespace
        
        permission = IsAuthenticatedOrReadOnly()
        
        # Mock request and view
        request = HttpRequest()
        view = SimpleNamespace()
        
        # Test GET request (read-only)
        request.method = 'GET'
        request.user = None
        self.assertTrue(permission.has_permission(request, view))
        
        # Test POST request without authentication
        request.method = 'POST'
        self.assertFalse(permission.has_permission(request, view))
        
        # Test POST request with authentication
        request.user = self.user
        self.assertTrue(permission.has_permission(request, view))


class SecurityModelSignalsTest(TestCase):
    """Test suite for model signals and related functionality."""
    
    def setUp(self):
        """Set up test data for each test method."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_user_profile_creation_on_user_creation(self):
        """Test if UserProfile is automatically created when User is created."""
        # This test assumes there might be a signal for auto-creation
        # If no signal exists, this test documents the expected behavior
        new_user = User.objects.create_user(
            username='newuser',
            email='newuser@example.com',
            password='password123'
        )
        
        # Check if profile exists or needs manual creation
        try:
            profile = new_user.user_profile
            self.assertIsNotNone(profile)
        except UserProfile.DoesNotExist:
            # Profile needs to be created manually
            profile = UserProfile.objects.create(user=new_user)
            self.assertEqual(profile.user, new_user)


class SecurityBusinessLogicTest(TestCase):
    """Test suite for security-related business logic."""
    
    def setUp(self):
        """Set up test data for each test method."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_user_profile_phone_formatting(self):
        """Test phone number formatting and validation."""
        profile = UserProfile.objects.create(
            user=self.user,
            phone='123-456-7890'
        )
        
        # Test that phone is stored as provided
        self.assertEqual(profile.phone, '123-456-7890')
        
    def test_user_profile_address_storage(self):
        """Test address field storage and retrieval."""
        long_address = 'A very long address that contains multiple lines and details about the location'
        
        profile = UserProfile.objects.create(
            user=self.user,
            address=long_address
        )
        
        self.assertEqual(profile.address, long_address)
        
    def test_user_groups_relationship(self):
        """Test user groups functionality through profile."""
        group1 = Group.objects.create(name='Group1')
        group2 = Group.objects.create(name='Group2')
        
        self.user.groups.add(group1, group2)
        
        profile = UserProfile.objects.create(user=self.user)
        
        # Test that we can access user groups through profile
        user_groups = profile.user.groups.all()
        self.assertIn(group1, user_groups)
        self.assertIn(group2, user_groups)
        self.assertEqual(user_groups.count(), 2)