#!/usr/bin/env python
"""
Test script for Twilio integration
"""

import os
import sys
import django
from django.conf import settings

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.support.messaging.services.twilio_service import TwilioService
from django.contrib.auth.models import User

def test_twilio_service():
    """Test the Twilio service functionality"""
    print("Testing Twilio Service...")
    
    # Initialize the service
    service = TwilioService()
    
    print(f"Twilio enabled: {service.is_enabled()}")
    
    if not service.is_enabled():
        print("Twilio is not configured. Please set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_PHONE_NUMBER in your environment.")
        return
    
    # Test OTP generation
    otp = service.generate_otp()
    print(f"Generated OTP: {otp}")
    
    # Test with a real user if available
    try:
        user = User.objects.first()
        if user:
            print(f"Testing with user: {user.username}")
        else:
            print("No users found in database")
    except Exception as e:
        print(f"Error getting user: {e}")

if __name__ == "__main__":
    test_twilio_service()