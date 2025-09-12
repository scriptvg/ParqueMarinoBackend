from django.test import TestCase, TransactionTestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Group, Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date, datetime
from .models import UserProfile


class UserProfileModelTest(TestCase):
    """Test suite for UserProfile model functionality."""
    
    def setUp(self):
        """Set up test data for each test method."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_user_profile_creation(self):
        """Test basic UserProfile creation."""
        profile = UserProfile.objects.create(
            user=self.user,
            phone='1234567890',
            address='123 Test Street',
            birth_date=date(1990, 1, 1)
        )
        
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.phone, '1234567890')
        self.assertEqual(profile.address, '123 Test Street')
        self.assertEqual(profile.birth_date, date(1990, 1, 1))
        
    def test_user_profile_str_representation(self):
        """Test UserProfile string representation."""
        profile = UserProfile.objects.create(
            user=self.user,
            phone='1234567890'
        )
        
        expected_str = f'Perfil de {self.user.username}'
        self.assertEqual(str(profile), expected_str)
        
    def test_user_profile_optional_fields(self):
        """Test UserProfile creation with optional fields as None/blank."""
        profile = UserProfile.objects.create(
            user=self.user
        )
        
        self.assertIsNone(profile.phone)
        self.assertIsNone(profile.address)
        self.assertIsNone(profile.birth_date)
        self.assertFalse(profile.profile_picture)
        
    def test_user_profile_phone_max_length(self):
        """Test phone field max length validation."""
        long_phone = '1' * 21  # 21 characters, exceeds max_length=20
        
        profile = UserProfile(
            user=self.user,
            phone=long_phone
        )
        
        with self.assertRaises(ValidationError):
            profile.full_clean()
            
    def test_user_profile_address_max_length(self):
        """Test address field max length validation."""
        long_address = 'A' * 201  # 201 characters, exceeds max_length=200
        
        profile = UserProfile(
            user=self.user,
            address=long_address
        )
        
        with self.assertRaises(ValidationError):
            profile.full_clean()
            
    def test_user_profile_with_image(self):
        """Test UserProfile creation with profile picture."""
        # Create a simple test image file
        image_content = b'fake_image_content'
        image_file = SimpleUploadedFile(
            'test_profile.jpg',
            image_content,
            content_type='image/jpeg'
        )
        
        profile = UserProfile.objects.create(
            user=self.user,
            profile_picture=image_file
        )
        
        self.assertTrue(profile.profile_picture)
        self.assertIn('profile_pictures/', profile.profile_picture.name)
        
    def test_user_profile_one_to_one_relationship(self):
        """Test that UserProfile has a proper OneToOne relationship with User."""
        profile = UserProfile.objects.create(
            user=self.user,
            phone='1234567890'
        )
        
        # Test forward relationship
        self.assertEqual(profile.user, self.user)
        
        # Test reverse relationship
        self.assertEqual(self.user.user_profile, profile)
        
    def test_user_profile_unique_user_constraint(self):
        """Test that each User can have only one UserProfile."""
        # Create first profile
        UserProfile.objects.create(
            user=self.user,
            phone='1234567890'
        )
        
        # Try to create second profile for same user
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                UserProfile.objects.create(
                    user=self.user,
                    phone='0987654321'
                )
                
    def test_user_profile_cascade_delete(self):
        """Test that UserProfile is deleted when User is deleted."""
        profile = UserProfile.objects.create(
            user=self.user,
            phone='1234567890'
        )
        
        profile_id = profile.id
        
        # Delete the user
        self.user.delete()
        
        # Profile should be deleted too
        with self.assertRaises(UserProfile.DoesNotExist):
            UserProfile.objects.get(id=profile_id)
            
    def test_user_profile_meta_options(self):
        """Test UserProfile model meta options."""
        profile = UserProfile.objects.create(
            user=self.user,
            phone='1234567890'
        )
        
        # Test db_table
        self.assertEqual(profile._meta.db_table, 'user_profile')
        
        # Test verbose names
        self.assertEqual(profile._meta.verbose_name, 'Perfil de usuario')
        self.assertEqual(profile._meta.verbose_name_plural, 'Perfiles de usuarios')
        
    def test_user_profile_blank_fields_allowed(self):
        """Test that blank values are allowed for optional fields."""
        profile = UserProfile.objects.create(
            user=self.user,
            phone='',  # blank string
            address='',  # blank string
            birth_date=None  # null value
        )
        
        # Should save without validation errors
        profile.full_clean()
        profile.save()
        
        self.assertEqual(profile.phone, '')
        self.assertEqual(profile.address, '')
        self.assertIsNone(profile.birth_date)
        
    def test_user_profile_future_birth_date(self):
        """Test UserProfile with future birth date (should be allowed by model)."""
        future_date = date(2050, 1, 1)
        
        profile = UserProfile.objects.create(
            user=self.user,
            birth_date=future_date
        )
        
        # Model allows future dates, business logic validation should be in serializers/forms
        self.assertEqual(profile.birth_date, future_date)
        
    def test_user_profile_related_name(self):
        """Test the related_name for the User-UserProfile relationship."""
        profile = UserProfile.objects.create(
            user=self.user,
            phone='1234567890'
        )
        
        # Test that related_name 'user_profile' works
        self.assertEqual(self.user.user_profile, profile)
        
    def test_multiple_user_profiles(self):
        """Test creating profiles for multiple users."""
        user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        
        profile1 = UserProfile.objects.create(
            user=self.user,
            phone='1111111111'
        )
        
        profile2 = UserProfile.objects.create(
            user=user2,
            phone='2222222222'
        )
        
        self.assertEqual(UserProfile.objects.count(), 2)
        self.assertEqual(profile1.user, self.user)
        self.assertEqual(profile2.user, user2)
        self.assertNotEqual(profile1.phone, profile2.phone)
