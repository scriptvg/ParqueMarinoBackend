# Sistema de Notificaciones Simplificado

## Descripción

Este documento explica cómo funciona el sistema de notificaciones simplificado para el sistema de pagos. En lugar de enviar emails, el sistema ahora devuelve datos que pueden ser utilizados por el frontend para mostrar alertas y notificaciones al usuario.

## Componentes

### 1. PaymentNotifier (Clase)

El archivo `payments/notifications.py` contiene la clase `PaymentNotifier` que genera objetos de notificación simples en lugar de enviar emails.

#### Métodos Disponibles:

1. `send_payment_confirmation(payment_data)`: Genera una notificación de pago exitoso
2. `send_payment_failed(payment_data)`: Genera una notificación de pago fallido
3. `send_invoice(invoice_data)`: Genera una notificación de factura generada
4. `send_refund_confirmation(refund_data)`: Genera una notificación de reembolso procesado

#### Formato de Notificación:

```javascript
{
    "type": "success|error|info",
    "title": "Título de la notificación",
    "message": "Mensaje descriptivo",
    "payment_id|invoice_id|refund_id": "ID del elemento",
    "timestamp": "Fecha y hora"
}
```

### 2. Uso en los ViewSets

Los ViewSets en `payments/views.py` han sido actualizados para incluir notificaciones en sus respuestas:

#### Ejemplo de Respuesta Exitosa:

```json
{
    "message": "Pago procesado exitosamente",
    "payment_intent_id": "pi_XXXXXXXXXXXXXXXX",
    "client_secret": "pi_XXXXXXXXXXXXXXXX_secret_YYYYYYYYYYYYYYYY",
    "notification": {
        "type": "success",
        "title": "Pago Confirmado",
        "message": "El pago de 100.00 USD se ha procesado exitosamente.",
        "payment_id": 1,
        "timestamp": "2023-01-01T10:00:00Z"
    }
}
```

#### Ejemplo de Respuesta con Error:

```json
{
    "error": "Error al procesar el pago: ...",
    "notification": {
        "type": "error",
        "title": "Pago Fallido",
        "message": "El pago de 100.00 USD no se pudo procesar.",
        "payment_id": 1,
        "timestamp": "2023-01-01T10:00:00Z"
    }
}
```

## Implementación en el Frontend

### 1. JavaScript Básico

El archivo `FRONTEND_NOTIFICATIONS_EXAMPLE.js` muestra cómo implementar el sistema de notificaciones en el frontend:

```javascript
// Función para mostrar notificaciones en la UI
function showNotification(notification) {
    // Crea y muestra una notificación en la interfaz
}

// Función para procesar un pago
async function processGeneralPayment(paymentId) {
    try {
        const response = await fetch(`/api/payments/pagos/${paymentId}/procesar_pago/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('access_token')
            }
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Mostrar notificación de éxito
            showNotification(data.notification);
        } else {
            // Mostrar notificación de error
            showNotification(data.notification);
        }
    } catch (error) {
        // Mostrar notificación de error de red
        showNotification({ 
            type: 'error', 
            title: 'Error de Conexión', 
            message: 'No se pudo conectar con el servidor' 
        });
    }
}
```

### 2. HTML de Demostración

El archivo `FRONTEND_NOTIFICATIONS_DEMO.html` proporciona un ejemplo completo de cómo implementar el sistema de notificaciones en una interfaz web.

## Beneficios del Sistema Simplificado

1. **Menor Complejidad**: No requiere configuración de servidor de correo
2. **Respuesta Inmediata**: Las notificaciones se muestran instantáneamente al usuario
3. **Personalización**: Fácil de personalizar el estilo y comportamiento en el frontend
4. **Sin Dependencias Externas**: No requiere servicios de email externos
5. **Mejor Experiencia de Usuario**: Las notificaciones son más visibles y contextuales

## Futura Implementación de Emails

Para implementar el envío de emails en el futuro:

1. Restaurar el código original en `payments/notifications.py`
2. Configurar las variables de entorno para el servidor de correo
3. Actualizar los ViewSets para enviar emails además de devolver notificaciones
4. Mantener las notificaciones para el frontend

## Ejemplo de Uso Futuro con Emails

```python
# En el futuro, se podría tener ambos sistemas:
def procesar_pago(self, request, pk=None):
    # ... procesamiento del pago ...
    
    # Notificación para el frontend
    notifier = PaymentNotifier()
    notification = notifier.send_payment_confirmation(payment_data)
    
    # Email (para futura implementación)
    # email_notifier = PaymentEmailNotifier()
    # email_notifier.send_payment_confirmation(payment_data, user_email)
    
    return Response({
        'message': 'Pago procesado exitosamente',
        'notification': notification
    })
```

## Conclusión

El sistema de notificaciones simplificado proporciona una solución ligera y efectiva para informar a los usuarios sobre el estado de sus pagos sin la complejidad de configurar un sistema de emails. Es fácil de implementar, personalizar y extender en el futuro si se decide agregar emails.