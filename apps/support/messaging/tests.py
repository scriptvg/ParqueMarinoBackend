from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import OTPRecord
from .services.twilio_service import TwilioService
from datetime import timedelta
from django.utils import timezone
import random
from unittest.mock import patch, MagicMock

class OTPRecordModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_otp_record_creation(self):
        """Test creating an OTP record"""
        phone_number = '+1234567890'
        otp_code = '123456'
        
        otp_record = OTPRecord.objects.create(
            user=self.user,
            phone_number=phone_number,
            otp_code=otp_code,
            purpose='registration'
        )
        
        self.assertEqual(otp_record.user, self.user)
        self.assertEqual(otp_record.phone_number, phone_number)
        self.assertEqual(otp_record.otp_code, otp_code)
        self.assertEqual(otp_record.purpose, 'registration')
        self.assertFalse(otp_record.is_verified)
        
        # Check that expires_at is set automatically
        self.assertIsNotNone(otp_record.expires_at)
    
    def test_otp_expiration(self):
        """Test OTP expiration logic"""
        # Create an OTP that expires in 5 minutes
        expires_at = timezone.now() + timedelta(minutes=5)
        otp_record = OTPRecord.objects.create(
            user=self.user,
            phone_number='+1234567890',
            otp_code='123456',
            expires_at=expires_at,
            purpose='registration'
        )
        
        # Should not be expired yet
        self.assertFalse(otp_record.is_expired())
        
        # Create an expired OTP
        expired_otp = OTPRecord.objects.create(
            user=self.user,
            phone_number='+1234567890',
            otp_code='123456',
            expires_at=timezone.now() - timedelta(minutes=5),
            purpose='registration'
        )
        
        # Should be expired
        self.assertTrue(expired_otp.is_expired())

class TwilioServiceTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_generate_otp(self):
        """Test OTP generation"""
        service = TwilioService()
        otp = service.generate_otp()
        
        # Check that OTP is a 6-digit string
        self.assertEqual(len(otp), 6)
        self.assertTrue(otp.isdigit())
    
    def test_is_enabled_without_credentials(self):
        """Test that service is disabled without credentials"""
        service = TwilioService()
        # Since we don't have credentials in test environment
        self.assertFalse(service.is_enabled())
    
    @patch('apps.support.messaging.services.twilio_service.Client')
    def test_send_otp_sms_success(self, mock_client):
        """Test successful OTP SMS sending"""
        # Mock Twilio client
        mock_message_instance = MagicMock()
        mock_message_instance.sid = 'SM1234567890'
        mock_client_instance = MagicMock()
        mock_client_instance.messages.create.return_value = mock_message_instance
        mock_client.return_value = mock_client_instance
        
        # Create service with mock credentials
        service = TwilioService()
        service.account_sid = 'test_sid'
        service.auth_token = 'test_token'
        service.from_number = '+1234567890'
        service.client = mock_client_instance
        
        # Test sending OTP
        success, message, otp_record = service.send_otp_sms(
            '+18777804236', self.user, 'registration'
        )
        
        # Assertions
        self.assertTrue(success)
        self.assertEqual(message, 'OTP sent successfully')
        self.assertIsNotNone(otp_record)
        self.assertEqual(otp_record.phone_number, '+18777804236')
        self.assertEqual(otp_record.purpose, 'registration')
        
        # Verify Twilio API was called
        mock_client_instance.messages.create.assert_called_once()
    
    @patch('apps.support.messaging.services.twilio_service.Client')
    def test_verify_otp_success(self, mock_client):
        """Test successful OTP verification"""
        # Create an OTP record first
        otp_code = '123456'
        otp_record = OTPRecord.objects.create(
            user=self.user,
            phone_number='+18777804236',
            otp_code=otp_code,
            purpose='registration'
        )
        
        # Create service
        service = TwilioService()
        
        # Test verification
        is_valid, message = service.verify_otp(
            '+18777804236', otp_code, self.user, 'registration'
        )
        
        # Assertions
        self.assertTrue(is_valid)
        self.assertEqual(message, 'OTP verified successfully')
        
        # Refresh from database and check if verified
        otp_record.refresh_from_db()
        self.assertTrue(otp_record.is_verified)
    
    def test_verify_otp_expired(self):
        """Test OTP verification with expired OTP"""
        # Create an expired OTP record
        otp_code = '123456'
        expired_otp = OTPRecord.objects.create(
            user=self.user,
            phone_number='+18777804236',
            otp_code=otp_code,
            expires_at=timezone.now() - timedelta(minutes=5),
            purpose='registration'
        )
        
        # Create service
        service = TwilioService()
        
        # Test verification
        is_valid, message = service.verify_otp(
            '+18777804236', otp_code, self.user, 'registration'
        )
        
        # Assertions
        self.assertFalse(is_valid)
        self.assertEqual(message, 'OTP has expired')

class MessagingAPITest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    @patch('apps.support.messaging.services.twilio_service.TwilioService.is_enabled')
    @patch('apps.support.messaging.services.twilio_service.TwilioService.send_otp_sms')
    def test_send_otp_success(self, mock_send_otp, mock_is_enabled):
        """Test successful OTP sending via API"""
        # Mock service methods
        mock_is_enabled.return_value = True
        mock_otp_record = MagicMock()
        mock_otp_record.id = 1
        mock_send_otp.return_value = (True, 'OTP sent successfully', mock_otp_record)
        
        # Make API request
        response = self.client.post(
            reverse('messaging:send-otp'),
            {
                'phone_number': '+18777804236',
                'purpose': 'registration'
            },
            format='json'
        )
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'OTP sent successfully')
        self.assertEqual(response.data['otp_id'], 1)
    
    @patch('apps.support.messaging.services.twilio_service.TwilioService.is_enabled')
    def test_send_otp_service_disabled(self, mock_is_enabled):
        """Test OTP sending when service is disabled"""
        # Mock service as disabled
        mock_is_enabled.return_value = False
        
        # Make API request
        response = self.client.post(
            reverse('messaging:send-otp'),
            {
                'phone_number': '+18777804236',
                'purpose': 'registration'
            },
            format='json'
        )
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertEqual(response.data['error'], 'SMS service is not configured')
    
    @patch('apps.support.messaging.services.twilio_service.TwilioService.verify_otp')
    def test_verify_otp_success(self, mock_verify_otp):
        """Test successful OTP verification via API"""
        # Mock service method
        mock_verify_otp.return_value = (True, 'OTP verified successfully')
        
        # Make API request
        response = self.client.post(
            reverse('messaging:verify-otp'),
            {
                'phone_number': '+18777804236',
                'otp_code': '123456',
                'purpose': 'registration'
            },
            format='json'
        )
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'OTP verified successfully')
        self.assertTrue(response.data['verified'])
    
    def test_send_otp_unauthorized(self):
        """Test OTP sending without authentication"""
        # Create unauthenticated client
        unauth_client = APIClient()
        
        # Make API request
        response = unauth_client.post(
            reverse('messaging:send-otp'),
            {
                'phone_number': '+18777804236',
                'purpose': 'registration'
            },
            format='json'
        )
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)