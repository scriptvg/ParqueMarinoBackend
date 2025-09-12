# Ejemplo de Frontend para Integración con Stripe

## Descripción

Este ejemplo muestra cómo implementar el frontend para completar pagos usando la integración con Stripe.

## HTML Básico

```html
<!DOCTYPE html>
<html>
<head>
    <title>Pago con Stripe</title>
    <script src="https://js.stripe.com/v3/"></script>
</head>
<body>
    <h1>Completar Pago</h1>
    <div id="payment-form">
        <div id="card-element">
            <!-- Elemento de Stripe se insertará aquí -->
        </div>
        <button id="submit-payment">Pagar</button>
        <div id="payment-errors" role="alert"></div>
    </div>
    
    <script src="payment.js"></script>
</body>
</html>
```

## JavaScript para Procesar Pagos

```javascript
// payment.js

// Inicializar Stripe con la clave pública
const stripe = Stripe('pk_test_pk_test_example_public_key_here'); // Reemplazar con tu clave pública real
const elements = stripe.elements();

// Crear un elemento de tarjeta
const cardElement = elements.create('card');
cardElement.mount('#card-element');

// Manejar errores
cardElement.on('change', ({error}) => {
    const displayError = document.getElementById('payment-errors');
    if (error) {
        displayError.textContent = error.message;
    } else {
        displayError.textContent = '';
    }
});

// Manejar el envío del pago
const submitButton = document.getElementById('submit-payment');
submitButton.addEventListener('click', async (event) => {
    event.preventDefault();
    
    // Deshabilitar el botón mientras se procesa
    submitButton.disabled = true;
    
    try {
        // Paso 1: Crear el pago en el backend
        const pagoData = {
            monto: 100.00,
            moneda: 'USD',
            metodo_pago: 'CARD',
            referencia_transaccion: 'REF' + Date.now()
        };
        
        const pagoResponse = await fetch('/api/payments/pagos/create/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('access_token') // Si usas autenticación JWT
            },
            body: JSON.stringify(pagoData)
        });
        
        if (!pagoResponse.ok) {
            throw new Error('Error al crear el pago');
        }
        
        const pago = await pagoResponse.json();
        const pagoId = pago.id;
        
        // Paso 2: Procesar el pago con Stripe
        const procesarResponse = await fetch(`/api/payments/pagos/${pagoId}/procesar_pago/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('access_token')
            }
        });
        
        if (!procesarResponse.ok) {
            throw new Error('Error al procesar el pago con Stripe');
        }
        
        const procesarData = await procesarResponse.json();
        const clientSecret = procesarData.client_secret;
        
        // Paso 3: Confirmar el pago con Stripe
        const {error, paymentIntent} = await stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: cardElement,
                billing_details: {
                    name: 'Nombre del Cliente'
                }
            }
        });
        
        if (error) {
            // Mostrar error al usuario
            document.getElementById('payment-errors').textContent = error.message;
        } else {
            // Pago exitoso
            if (paymentIntent.status === 'succeeded') {
                alert('¡Pago completado exitosamente!');
                // Redirigir a página de confirmación o actualizar UI
            }
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('payment-errors').textContent = 'Ocurrió un error al procesar el pago';
    } finally {
        // Rehabilitar el botón
        submitButton.disabled = false;
    }
});
```

## Para Pagos de Inscripción

```javascript
// Ejemplo para pagos de inscripción
async function procesarPagoInscripcion(inscripcionId, monto) {
    try {
        // Paso 1: Crear el pago de inscripción
        const pagoData = {
            inscripcion: inscripcionId,
            monto: monto,
            moneda: 'CRC',
            metodo_pago: 'CARD'
        };
        
        const pagoResponse = await fetch('/api/payments/pagos-inscripcion/create/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('access_token')
            },
            body: JSON.stringify(pagoData)
        });
        
        if (!pagoResponse.ok) {
            throw new Error('Error al crear el pago de inscripción');
        }
        
        const pago = await pagoResponse.json();
        const pagoId = pago.id;
        
        // Paso 2: Procesar el pago con Stripe
        const procesarResponse = await fetch(`/api/payments/pagos-inscripcion/${pagoId}/procesar_pago/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('access_token')
            }
        });
        
        if (!procesarResponse.ok) {
            throw new Error('Error al procesar el pago con Stripe');
        }
        
        const procesarData = await procesarResponse.json();
        const clientSecret = procesarData.client_secret;
        
        // Paso 3: Confirmar el pago con Stripe
        const {error, paymentIntent} = await stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: cardElement,
                billing_details: {
                    name: 'Nombre del Participante'
                }
            }
        });
        
        if (error) {
            document.getElementById('payment-errors').textContent = error.message;
        } else {
            if (paymentIntent.status === 'succeeded') {
                alert('¡Pago de inscripción completado exitosamente!');
                // Actualizar UI para mostrar confirmación
            }
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('payment-errors').textContent = 'Ocurrió un error al procesar el pago de inscripción';
    }
}
```

## Para Donaciones

```javascript
// Ejemplo para donaciones
async function procesarDonacion(monto, nombre, email) {
    try {
        // Paso 1: Crear la donación
        const donacionData = {
            monto: monto,
            moneda: 'USD',
            nombre_donante: nombre,
            email_donante: email,
            metodo_pago: 'CARD'
        };
        
        const donacionResponse = await fetch('/api/payments/donaciones/create/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(donacionData)
        });
        
        if (!donacionResponse.ok) {
            throw new Error('Error al crear la donación');
        }
        
        const donacion = await donacionResponse.json();
        const donacionId = donacion.id;
        
        // Paso 2: Procesar la donación con Stripe
        const procesarResponse = await fetch(`/api/payments/donaciones/${donacionId}/procesar_pago/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (!procesarResponse.ok) {
            throw new Error('Error al procesar la donación con Stripe');
        }
        
        const procesarData = await procesarResponse.json();
        const clientSecret = procesarData.client_secret;
        
        // Paso 3: Confirmar el pago con Stripe
        const {error, paymentIntent} = await stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: cardElement,
                billing_details: {
                    name: nombre,
                    email: email
                }
            }
        });
        
        if (error) {
            document.getElementById('payment-errors').textContent = error.message;
        } else {
            if (paymentIntent.status === 'succeeded') {
                alert('¡Gracias por tu donación!');
                // Limpiar formulario o mostrar mensaje de agradecimiento
            }
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('payment-errors').textContent = 'Ocurrió un error al procesar la donación';
    }
}
```

## Consideraciones Importantes

1. **Clave Pública**: Asegúrate de usar la clave pública correcta de Stripe
2. **Autenticación**: Implementa la autenticación adecuada según tu aplicación
3. **Manejo de Errores**: Implementa un manejo de errores robusto para todos los casos
4. **Seguridad**: Nunca expongas la clave secreta de Stripe en el frontend
5. **Validación**: Valida los datos del formulario antes de enviarlos al backend
6. **UX**: Proporciona feedback visual durante el proceso de pago

## Recursos Adicionales

- [Documentación de Stripe](https://stripe.com/docs)
- [Stripe Elements](https://stripe.com/docs/stripe-js)
- [Mejores Prácticas de Seguridad](https://stripe.com/docs/security)