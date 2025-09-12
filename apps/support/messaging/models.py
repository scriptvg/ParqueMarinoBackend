from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class OTPRecord(models.Model):
    """
    Model to store OTP records for phone verification
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otp_records')
    phone_number = models.CharField(max_length=20)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)
    purpose = models.CharField(max_length=50, choices=[
        ('registration', 'User Registration'),
        ('login', 'User Login'),
        ('password_reset', 'Password Reset'),
        ('phone_verification', 'Phone Verification')
    ])
    
    class Meta:
        db_table = 'otp_records'
        verbose_name = 'OTP Record'
        verbose_name_plural = 'OTP Records'
        indexes = [
            models.Index(fields=['phone_number', 'otp_code']),
            models.Index(fields=['user', 'purpose']),
        ]
    
    def save(self, *args, **kwargs):
        # Set expiration time to 10 minutes from now if not set
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=10)
        super().save(*args, **kwargs)
    
    def is_expired(self):
        """Check if the OTP has expired"""
        return timezone.now() > self.expires_at
    
    def __str__(self):
        return f"OTP for {self.phone_number} - {self.purpose}"