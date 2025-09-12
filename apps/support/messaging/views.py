import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import OTPRequestSerializer, OTPVerifySerializer
from .services.twilio_service import TwilioService
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

class SendOTPView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = OTPRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        phone_number = serializer.validated_data['phone_number']
        purpose = serializer.validated_data['purpose']
        
        # Initialize Twilio service
        twilio_service = TwilioService()
        
        if not twilio_service.is_enabled():
            return Response(
                {"error": "SMS service is not configured"}, 
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        # Send OTP
        success, message, otp_record = twilio_service.send_otp_sms(
            phone_number, request.user, purpose
        )
        
        if success:
            return Response({
                "message": message,
                "otp_id": otp_record.id if otp_record else None
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "error": message
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VerifyOTPView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        phone_number = serializer.validated_data['phone_number']
        otp_code = serializer.validated_data['otp_code']
        purpose = serializer.validated_data['purpose']
        
        # Initialize Twilio service
        twilio_service = TwilioService()
        
        # Verify OTP
        is_valid, message = twilio_service.verify_otp(
            phone_number, otp_code, request.user, purpose
        )
        
        if is_valid:
            return Response({
                "message": message,
                "verified": True
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "error": message,
                "verified": False
            }, status=status.HTTP_400_BAD_REQUEST)

class TestTwilioView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # This should be restricted to admin users in production
        if not request.user.is_staff:
            return Response(
                {"error": "Access denied"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        twilio_service = TwilioService()
        
        if not twilio_service.is_enabled():
            return Response(
                {"error": "Twilio is not configured"}, 
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        # Try to send a test message to the user's phone number if available
        user_profile = getattr(request.user, 'user_profile', None)
        phone_number = None
        if user_profile and user_profile.phone:
            phone_number = user_profile.phone
        else:
            # Fallback to a test number from environment variables
            import os
            phone_number = os.getenv('TEST_PHONE_NUMBER')
        
        if not phone_number:
            return Response(
                {"error": "No phone number available for testing"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        success, message = twilio_service.send_test_message(phone_number)
        
        if success:
            return Response({"message": message}, status=status.HTTP_200_OK)
        else:
            return Response({"error": message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)