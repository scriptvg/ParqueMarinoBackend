from django.urls import path
from apps.support.messaging.views import SendOTPView, VerifyOTPView, TestTwilioView

app_name = 'messaging'

urlpatterns = [
    path('send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('test-twilio/', TestTwilioView.as_view(), name='test-twilio'),
]