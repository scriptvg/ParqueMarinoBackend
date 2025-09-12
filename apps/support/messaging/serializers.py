from rest_framework import serializers
from .models import OTPRecord

class OTPRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)
    purpose = serializers.ChoiceField(choices=[
        ('registration', 'User Registration'),
        ('login', 'User Login'),
        ('password_reset', 'Password Reset'),
        ('phone_verification', 'Phone Verification')
    ])

class OTPVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)
    otp_code = serializers.CharField(max_length=6)
    purpose = serializers.ChoiceField(choices=[
        ('registration', 'User Registration'),
        ('login', 'User Login'),
        ('password_reset', 'Password Reset'),
        ('phone_verification', 'Phone Verification')
    ])

class OTPResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPRecord
        fields = ['id', 'phone_number', 'created_at', 'expires_at', 'is_verified', 'purpose']