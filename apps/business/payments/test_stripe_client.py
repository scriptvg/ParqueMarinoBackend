"""
Test para verificar que el cliente de Stripe funciona correctamente.
Este test puede ejecutarse independientemente del framework Django.
"""

import os
import sys
import django
from decimal import Decimal

# Configurar el entorno de Django
sys.path.append('c:\\Users\\velez\\OneDrive\\Desktop\\parque-marino\\old\\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.integrations.payments.stripe_client import StripeClient, StripeError

def test_stripe_client_initialization():
    """Test para verificar que el cliente de Stripe se inicializa correctamente."""
    try:
        client = StripeClient()
        print("✓ Cliente de Stripe inicializado correctamente")
        print(f"  Public Key: {client.public_key[:10]}...")
        print(f"  Secret Key: {client.api_key[:10]}...")
        return True
    except Exception as e:
        print(f"✗ Error al inicializar el cliente de Stripe: {e}")
        return False

def test_stripe_client_create_payment_intent():
    """Test para verificar que se puede crear una intención de pago."""
    try:
        client = StripeClient()
        
        # Crear una intención de pago de prueba
        payment_intent = client.create_payment_intent(
            amount=Decimal('100.00'),
            currency='usd',
            description='Test payment'
        )
        
        print("✓ Intención de pago creada correctamente")
        print(f"  ID: {payment_intent['id']}")
        print(f"  Amount: {payment_intent['amount']}")
        print(f"  Currency: {payment_intent['currency']}")
        print(f"  Status: {payment_intent['status']}")
        return True
    except StripeError as e:
        print(f"✗ Error de Stripe al crear intención de pago: {e}")
        return False
    except Exception as e:
        print(f"✗ Error inesperado al crear intención de pago: {e}")
        return False

if __name__ == "__main__":
    print("=== Test del Cliente de Stripe ===")
    print()
    
    # Test de inicialización
    init_success = test_stripe_client_initialization()
    print()
    
    # Test de creación de intención de pago
    if init_success:
        payment_success = test_stripe_client_create_payment_intent()
        print()
        
        if payment_success:
            print("=== Todos los tests pasaron ===")
        else:
            print("=== Algunos tests fallaron ===")
    else:
        print("=== No se puede continuar con los tests debido a error de inicialización ===")