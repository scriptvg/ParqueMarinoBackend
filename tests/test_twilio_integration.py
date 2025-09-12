#!/usr/bin/env python
"""
Test script for Twilio integration with test credentials
"""

import os
import sys
import django
from django.conf import settings

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.support.messaging.services.twilio_service import TwilioService
from django.contrib.auth.models import User

def test_twilio_integration():
    """Test the Twilio integration with test credentials"""
    print("Testing Twilio Integration...")
    
    # Initialize the service
    service = TwilioService()
    
    print(f"Twilio enabled: {service.is_enabled()}")
    
    if not service.is_enabled():
        print("Twilio is not configured properly.")
        print("Please ensure you have set the following environment variables:")
        print("- TWILIO_ACCOUNT_SID")
        print("- TWILIO_AUTH_TOKEN")
        print("- TWILIO_PHONE_NUMBER")
        return
    
    # Test sending a message to the test number
    test_number = os.getenv('TEST_PHONE_NUMBER')
    if not test_number:
        print("TEST_PHONE_NUMBER environment variable not set")
        return
    
    print(f"Sending test message to: {test_number}")
    
    # Send a test message
    success, message = service.send_test_message(test_number)
    
    if success:
        print(f"Success: {message}")
    else:
        print(f"Error: {message}")

def test_otp_flow():
    """Test the full OTP flow"""
    print("\nTesting OTP Flow...")
    
    # Initialize the service
    service = TwilioService()
    
    if not service.is_enabled():
        print("Twilio is not configured properly.")
        return
    
    # Get a test user
    user = User.objects.first()
    if not user:
        print("No users found in database. Please create a user first.")
        return
    
    test_number = os.getenv('TEST_PHONE_NUMBER')
    if not test_number:
        print("TEST_PHONE_NUMBER environment variable not set")
        return
    
    print(f"Sending OTP to: {test_number}")
    
    # Send OTP
    success, message, otp_record = service.send_otp_sms(
        test_number, user, 'registration'
    )
    
    if success:
        print(f"OTP sent successfully: {message}")
        print(f"OTP Record ID: {otp_record.id}")
        print(f"OTP Code: {otp_record.otp_code}")
        
        # Test verification
        print(f"\nVerifying OTP: {otp_record.otp_code}")
        is_valid, verify_message = service.verify_otp(
            test_number, otp_record.otp_code, user, 'registration'
        )
        
        if is_valid:
            print(f"OTP verified successfully: {verify_message}")
        else:
            print(f"OTP verification failed: {verify_message}")
    else:
        print(f"Failed to send OTP: {message}")

if __name__ == "__main__":
    test_twilio_integration()
    test_otp_flow()