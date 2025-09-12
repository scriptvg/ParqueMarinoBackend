import sys
print("Python path:")
for path in sys.path:
    print(f"  {path}")

try:
    from twilio.rest import Client
    print("Twilio import successful!")
except ImportError as e:
    print(f"Twilio import failed: {e}")