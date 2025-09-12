/**
 * Ejemplo de cómo usar las notificaciones en el frontend
 * 
 * Este archivo muestra cómo manejar las notificaciones que vienen desde el backend
 * y mostrarlas como alertas en la interfaz de usuario.
 */

// Función para mostrar notificaciones en la UI
function showNotification(notification) {
    // Crear elemento de notificación
    const notificationElement = document.createElement('div');
    notificationElement.className = `notification notification-${notification.type}`;
    
    // Estilos básicos para las notificaciones
    const styles = {
        success: { backgroundColor: '#d4edda', color: '#155724', border: '1px solid #c3e6cb' },
        error: { backgroundColor: '#f8d7da', color: '#721c24', border: '1px solid #f5c6cb' },
        info: { backgroundColor: '#d1ecf1', color: '#0c5460', border: '1px solid #bee5eb' }
    };
    
    // Aplicar estilos
    Object.assign(notificationElement.style, {
        padding: '15px',
        margin: '10px 0',
        borderRadius: '4px',
        ...styles[notification.type]
    });
    
    // Contenido de la notificación
    notificationElement.innerHTML = `
        <strong>${notification.title}</strong>
        <p>${notification.message}</p>
        <small>ID: ${notification.payment_id || notification.invoice_id || notification.refund_id} - 
        ${new Date(notification.timestamp).toLocaleString()}</small>
    `;
    
    // Agregar al contenedor de notificaciones
    const notificationContainer = document.getElementById('notifications-container');
    if (notificationContainer) {
        notificationContainer.appendChild(notificationElement);
        
        // Remover automáticamente después de 5 segundos
        setTimeout(() => {
            if (notificationElement.parentNode) {
                notificationElement.parentNode.removeChild(notificationElement);
            }
        }, 5000);
    }
}

// Función para procesar un pago general
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
            
            // Aquí puedes agregar lógica adicional como redirigir al usuario
            // o actualizar la UI para mostrar el pago completado
            console.log('Pago procesado exitosamente:', data);
        } else {
            // Mostrar notificación de error
            showNotification(data.notification || { 
                type: 'error', 
                title: 'Error', 
                message: data.error || 'Error al procesar el pago' 
            });
        }
    } catch (error) {
        // Mostrar notificación de error de red
        showNotification({ 
            type: 'error', 
            title: 'Error de Conexión', 
            message: 'No se pudo conectar con el servidor' 
        });
        console.error('Error al procesar el pago:', error);
    }
}

// Función para procesar un pago de inscripción
async function processInscriptionPayment(paymentId) {
    try {
        const response = await fetch(`/api/payments/pagos-inscripcion/${paymentId}/procesar_pago/`, {
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
            
            // Aquí puedes agregar lógica adicional como redirigir al usuario
            // o actualizar la UI para mostrar el pago completado
            console.log('Pago de inscripción procesado exitosamente:', data);
        } else {
            // Mostrar notificación de error
            showNotification(data.notification || { 
                type: 'error', 
                title: 'Error', 
                message: data.error || 'Error al procesar el pago de inscripción' 
            });
        }
    } catch (error) {
        // Mostrar notificación de error de red
        showNotification({ 
            type: 'error', 
            title: 'Error de Conexión', 
            message: 'No se pudo conectar con el servidor' 
        });
        console.error('Error al procesar el pago de inscripción:', error);
    }
}

// Función para procesar una donación
async function processDonation(donationId) {
    try {
        const response = await fetch(`/api/payments/donaciones/${donationId}/procesar_pago/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
                // Las donaciones no requieren autenticación
            }
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Mostrar notificación de éxito
            showNotification(data.notification);
            
            // Aquí puedes agregar lógica adicional como redirigir al usuario
            // o actualizar la UI para mostrar la donación completada
            console.log('Donación procesada exitosamente:', data);
        } else {
            // Mostrar notificación de error
            showNotification(data.notification || { 
                type: 'error', 
                title: 'Error', 
                message: data.error || 'Error al procesar la donación' 
            });
        }
    } catch (error) {
        // Mostrar notificación de error de red
        showNotification({ 
            type: 'error', 
            title: 'Error de Conexión', 
            message: 'No se pudo conectar con el servidor' 
        });
        console.error('Error al procesar la donación:', error);
    }
}

// Ejemplo de cómo integrar con Stripe Elements
async function processPaymentWithStripe(paymentId, cardElement) {
    try {
        // Paso 1: Procesar el pago en el backend para obtener el client_secret
        const processResponse = await fetch(`/api/payments/pagos/${paymentId}/procesar_pago/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('access_token')
            }
        });
        
        const processData = await processResponse.json();
        
        if (!processResponse.ok) {
            // Mostrar notificación de error
            showNotification(processData.notification || { 
                type: 'error', 
                title: 'Error', 
                message: processData.error || 'Error al iniciar el proceso de pago' 
            });
            return;
        }
        
        // Paso 2: Confirmar el pago con Stripe
        const stripe = Stripe('pk_test_XXXXXXXXXXXXXXXXXXXXXXXX'); // Tu clave pública de Stripe
        const { error, paymentIntent } = await stripe.confirmCardPayment(
            processData.client_secret,
            {
                payment_method: {
                    card: cardElement,
                    billing_details: {
                        name: 'Nombre del Cliente'
                    }
                }
            }
        );
        
        if (error) {
            // Mostrar notificación de error de Stripe
            showNotification({ 
                type: 'error', 
                title: 'Error de Pago', 
                message: error.message || 'Error al procesar el pago con tarjeta' 
            });
            console.error('Error de Stripe:', error);
        } else {
            if (paymentIntent.status === 'succeeded') {
                // Mostrar notificación de éxito
                showNotification({
                    type: 'success',
                    title: 'Pago Completado',
                    message: 'El pago se ha procesado exitosamente',
                    payment_id: paymentId,
                    timestamp: new Date().toISOString()
                });
                
                // Aquí puedes redirigir al usuario a una página de confirmación
                // o actualizar la UI para mostrar el pago completado
                console.log('Pago completado con éxito');
            }
        }
    } catch (error) {
        // Mostrar notificación de error de red
        showNotification({ 
            type: 'error', 
            title: 'Error de Conexión', 
            message: 'No se pudo conectar con el servidor' 
        });
        console.error('Error al procesar el pago con Stripe:', error);
    }
}

// Función para inicializar el sistema de notificaciones
function initNotifications() {
    // Crear contenedor de notificaciones si no existe
    if (!document.getElementById('notifications-container')) {
        const container = document.createElement('div');
        container.id = 'notifications-container';
        container.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 10000;
            width: 300px;
        `;
        document.body.appendChild(container);
    }
}

// Inicializar cuando se cargue la página
document.addEventListener('DOMContentLoaded', function() {
    initNotifications();
});

// Exportar funciones para usar en otros archivos
export {
    showNotification,
    processGeneralPayment,
    processInscriptionPayment,
    processDonation,
    processPaymentWithStripe
};