import os
import logging
from twilio.rest import Client
from django.conf import settings
from ..models import OTPRecord
from django.contrib.auth.models import User
from django.utils import timezone
import random

logger = logging.getLogger(__name__)

class TwilioService:
    def __init__(self):
        # Get Twilio credentials from environment variables
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.from_number = os.getenv('TWILIO_PHONE_NUMBER')
        
        # Initialize Twilio client only if credentials are available
        if self.account_sid and self.auth_token:
            self.client = Client(self.account_sid, self.auth_token)
        else:
            self.client = None
            logger.warning("Twilio credentials not found. SMS functionality will be disabled.")
    
    def is_enabled(self):
        """Check if Twilio is properly configured"""
        return self.client is not None
    
    def generate_otp(self):
        """Generate a 6-digit OTP"""
        return str(random.randint(100000, 999999))
    
    def send_otp_sms(self, phone_number, user, purpose='phone_verification'):
        """
        Send OTP via SMS using Twilio
        Returns tuple: (success: bool, message: str, otp_record: OTPRecord)
        """
        if not self.is_enabled():
            return False, "Twilio is not configured", None
        
        try:
            # Generate OTP
            otp_code = self.generate_otp()
            
            # Create OTP record in database
            otp_record = OTPRecord.objects.create(
                user=user,
                phone_number=phone_number,
                otp_code=otp_code,
                purpose=purpose
            )
            
            # Prepare message
            message_body = f"Your verification code is: {otp_code}. Valid for 10 minutes."
            
            # Send SMS via Twilio
            message = self.client.messages.create(
                body=message_body,
                from_=self.from_number,
                to=phone_number
            )
            
            logger.info(f"OTP sent successfully to {phone_number} with SID: {message.sid}")
            return True, "OTP sent successfully", otp_record
            
        except Exception as e:
            logger.error(f"Failed to send OTP to {phone_number}: {str(e)}")
            return False, f"Failed to send OTP: {str(e)}", None
    
    def verify_otp(self, phone_number, otp_code, user, purpose='phone_verification'):
        """
        Verify OTP code
        Returns tuple: (is_valid: bool, message: str)
        """
        try:
            # Find the most recent OTP record for this phone number and user
            otp_record = OTPRecord.objects.filter(
                phone_number=phone_number,
                user=user,
                purpose=purpose,
                is_verified=False
            ).order_by('-created_at').first()
            
            if not otp_record:
                return False, "No OTP record found"
            
            # Check if OTP has expired
            if otp_record.is_expired():
                return False, "OTP has expired"
            
            # Check if OTP matches
            if otp_record.otp_code == otp_code:
                # Mark as verified
                otp_record.is_verified = True
                otp_record.save()
                return True, "OTP verified successfully"
            else:
                return False, "Invalid OTP code"
                
        except Exception as e:
            logger.error(f"Error verifying OTP for {phone_number}: {str(e)}")
            return False, f"Error verifying OTP: {str(e)}"
    
    def send_test_message(self, to_number):
        """
        Send a test message to verify Twilio configuration
        """
        if not self.is_enabled():
            return False, "Twilio is not configured"
        
        try:
            message = self.client.messages.create(
                body="Twilio integration test message from ParqueMarinoBackend",
                from_=self.from_number,
                to=to_number
            )
            return True, f"Test message sent successfully with SID: {message.sid}"
        except Exception as e:
            logger.error(f"Failed to send test message: {str(e)}")
            return False, f"Failed to send test message: {str(e)}"