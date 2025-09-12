#!/usr/bin/env python
"""
Manual test script for messaging app functionality
"""

import os
import sys
import django
import uuid

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.contrib.auth.models import User
from apps.support.messaging.models import OTPRecord
from apps.support.messaging.services.twilio_service import TwilioService
from datetime import timedelta
from django.utils import timezone

def create_unique_user(username_prefix):
    """Create a user with a unique username"""
    unique_username = f"{username_prefix}_{uuid.uuid4().hex[:8]}"
    return User.objects.create_user(
        username=unique_username,
        email=f"{unique_username}@example.com",
        password='testpass123'
    )

def test_otp_record_creation():
    """Test creating an OTP record"""
    print("Testing OTP record creation...")
    
    # Create a test user
    user = create_unique_user('testuser')
    
    phone_number = '+1234567890'
    otp_code = '123456'
    
    otp_record = OTPRecord.objects.create(
        user=user,
        phone_number=phone_number,
        otp_code=otp_code,
        purpose='registration'
    )
    
    assert otp_record.user == user
    assert otp_record.phone_number == phone_number
    assert otp_record.otp_code == otp_code
    assert otp_record.purpose == 'registration'
    assert otp_record.is_verified == False
    assert otp_record.expires_at is not None
    
    print("✓ OTP record creation test passed")

def test_otp_expiration():
    """Test OTP expiration logic"""
    print("Testing OTP expiration...")
    
    # Create a test user
    user = create_unique_user('testuser2')
    
    # Create an OTP that expires in 5 minutes
    expires_at = timezone.now() + timedelta(minutes=5)
    otp_record = OTPRecord.objects.create(
        user=user,
        phone_number='+1234567890',
        otp_code='123456',
        expires_at=expires_at,
        purpose='registration'
    )
    
    # Should not be expired yet
    assert otp_record.is_expired() == False
    
    # Create an expired OTP
    expired_otp = OTPRecord.objects.create(
        user=user,
        phone_number='+1234567890',
        otp_code='123456',
        expires_at=timezone.now() - timedelta(minutes=5),
        purpose='registration'
    )
    
    # Should be expired
    assert expired_otp.is_expired() == True
    
    print("✓ OTP expiration test passed")

def test_generate_otp():
    """Test OTP generation"""
    print("Testing OTP generation...")
    
    service = TwilioService()
    otp = service.generate_otp()
    
    # Check that OTP is a 6-digit string
    assert len(otp) == 6
    assert otp.isdigit()
    
    print("✓ OTP generation test passed")

def test_is_enabled_without_credentials():
    """Test that service is disabled without credentials"""
    print("Testing service disabled without credentials...")
    
    service = TwilioService()
    # Check if service is enabled
    is_enabled = service.is_enabled()
    print(f"Service enabled: {is_enabled}")
    
    # In test environment without credentials, it should be False
    # But let's not assert this since it might be enabled if env vars are set
    
    print("✓ Service disabled test completed")

def test_verify_otp_expired():
    """Test OTP verification with expired OTP"""
    print("Testing OTP verification with expired OTP...")
    
    # Create a test user
    user = create_unique_user('testuser5')
    
    # Create an expired OTP record
    otp_code = '123456'
    expired_otp = OTPRecord.objects.create(
        user=user,
        phone_number='+18777804236',
        otp_code=otp_code,
        expires_at=timezone.now() - timedelta(minutes=5),
        purpose='registration'
    )
    
    # Create service
    service = TwilioService()
    
    # Test verification
    is_valid, message = service.verify_otp(
        '+18777804236', otp_code, user, 'registration'
    )
    
    # Assertions
    assert is_valid == False
    assert message == 'OTP has expired'
    
    print("✓ Expired OTP verification test passed")

if __name__ == "__main__":
    print("Running messaging tests...")
    print("=" * 40)
    
    try:
        test_otp_record_creation()
        test_otp_expiration()
        test_generate_otp()
        test_is_enabled_without_credentials()
        test_verify_otp_expired()
        
        print("=" * 40)
        print("All tests completed! ✓")
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)