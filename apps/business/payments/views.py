# Importaciones de Django Rest Framework para vistas y utilidades
from rest_framework import viewsets, status
from rest_framework.decorators import action  # Para definir acciones personalizadas
from rest_framework.response import Response
from rest_framework.views import APIView

# Importaciones para manejo de permisos
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# Importaciones para filtrado y ordenamiento
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse

# Importaciones locales de modelos y serializadores
from .models import Pago, PagoInscripcion, Donacion
from .serializers import PagoSerializer, PagoInscripcionSerializer, DonacionSerializer
from apps.integrations.payments.stripe_client import StripeClient, StripeError
from .notifications import PaymentNotifier

class PagoViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar pagos generales
    
    Este ViewSet proporciona los siguientes endpoints:
    - GET /pagos/ - Lista todos los pagos (filtrado por usuario)
    - POST /pagos/ - Crea un nuevo pago
    - GET /pagos/{id}/ - Obtiene un pago específico
    - PUT /pagos/{id}/ - Actualiza un pago (solo admin)
    - DELETE /pagos/{id}/ - Elimina un pago (solo admin)
    - POST /pagos/{id}/procesar_pago/ - Procesa el pago con Stripe
    
    Permisos:
    - Listar y ver: Usuario autenticado
    - Crear: Usuario autenticado
    - Actualizar/Eliminar: Solo administradores
    
    Ejemplo de uso:
    ```python
    # Listar pagos (como usuario normal)
    GET /api/pagos/
    
    # Crear nuevo pago
    POST /api/pagos/
    {
        "monto": 50000,
        "moneda": "CRC",
        "metodo_pago": "TARJETA"
    }
    
    # Procesar pago
    POST /api/pagos/1/procesar_pago/
    ```
    """
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filtra los pagos según el tipo de usuario"""
        if self.request.user.is_staff:
            return Pago.objects.all()
        # Pago model doesn't have inscripcion field, so we filter by user directly
        return Pago.objects.filter(pagoinscripcion__isnull=True)  # Exclude inscription payments

    def get_permissions(self):
        """Define permisos según la acción"""
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def procesar_pago(self, request, pk=None):
        """Procesa un pago general utilizando Stripe
        
        Actualiza el estado del pago según el resultado del procesamiento con Stripe.
        """
        pago = self.get_object()
        
        # Solo procesar pagos que estén en estado pendiente
        if pago.estado != 'PENDING':
            return Response({
                'error': 'Este pago ya ha sido procesado'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Procesar pago con Stripe
        try:
            stripe_client = StripeClient()
            
            # Crear una intención de pago en Stripe
            currency = pago.moneda.lower()
            description = f"Pago general - {pago.referencia_transaccion}"
            
            # Convertir monto a la moneda correcta para Stripe
            amount = pago.monto
            if currency == 'crc':
                # Stripe requiere el monto en céntimos (colones * 100)
                amount_cents = int(amount)
            else:
                # Para USD, convertir a centavos
                amount_cents = int(amount * 100)
            
            # Crear la intención de pago
            payment_intent = stripe_client.create_payment_intent(
                amount=amount,
                currency=currency,
                description=description
            )
            
            # Actualizar el estado del pago
            pago.estado = 'SUCCESS'
            pago.referencia_transaccion = payment_intent['id']
            pago.save()
            
            # Generar notificación para el frontend
            notifier = PaymentNotifier()
            notification = notifier.send_payment_confirmation({
                'id': pago.id,
                'monto': str(pago.monto),
                'moneda': pago.moneda,
                'fecha_pago': pago.fecha_pago
            })
            
            return Response({
                'message': 'Pago procesado exitosamente',
                'payment_intent_id': payment_intent['id'],
                'client_secret': payment_intent['client_secret'],
                'notification': notification
            }, status=status.HTTP_200_OK)
            
        except StripeError as e:
            # Actualizar el estado del pago a fallido
            pago.estado = 'FAILED'
            pago.save()
            
            # Generar notificación de error para el frontend
            notifier = PaymentNotifier()
            notification = notifier.send_payment_failed({
                'id': pago.id,
                'monto': str(pago.monto),
                'moneda': pago.moneda,
                'fecha_pago': pago.fecha_pago
            })
            
            return Response({
                'error': str(e),
                'notification': notification
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Actualizar el estado del pago a fallido
            pago.estado = 'FAILED'
            pago.save()
            
            # Generar notificación de error para el frontend
            notifier = PaymentNotifier()
            notification = notifier.send_payment_failed({
                'id': pago.id,
                'monto': str(pago.monto),
                'moneda': pago.moneda,
                'fecha_pago': pago.fecha_pago
            })
            
            return Response({
                'error': f'Error al procesar el pago: {str(e)}',
                'notification': notification
            }, status=status.HTTP_400_BAD_REQUEST)

class PagoInscripcionViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar pagos de inscripciones a programas educativos
    
    Endpoints disponibles:
    - GET /pagos-inscripcion/ - Lista pagos de inscripción
    - POST /pagos-inscripcion/ - Crea pago de inscripción
    - GET /pagos-inscripcion/{id}/ - Obtiene detalles de un pago
    - PUT /pagos-inscripcion/{id}/ - Actualiza pago (admin)
    - DELETE /pagos-inscripcion/{id}/ - Elimina pago (admin)
    - POST /pagos-inscripcion/{id}/procesar_pago/ - Procesa el pago
    
    Funcionalidades especiales:
    - Validación automática del monto contra el precio del programa
    - Actualización del estado de la inscripción al procesar el pago
    - Filtrado de pagos por usuario actual
    
    Ejemplo de uso:
    ```python
    # Crear pago de inscripción
    POST /api/pagos-inscripcion/
    {
        "inscripcion": 1,
        "monto": 75000,
        "moneda": "CRC",
        "metodo_pago": "TARJETA"
    }
    
    # Procesar pago
    POST /api/pagos-inscripcion/1/procesar_pago/
    ```
    """
    queryset = PagoInscripcion.objects.all()
    serializer_class = PagoInscripcionSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def procesar_pago(self, request, pk=None):
        """Procesa el pago de una inscripción utilizando Stripe
        
        Actualiza el estado del pago y la inscripción según el resultado
        del procesamiento con Stripe.
        """
        pago = self.get_object()
        
        # Solo procesar pagos que estén en estado pendiente
        if pago.estado != 'PENDING':
            return Response({
                'error': 'Este pago ya ha sido procesado'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Procesar pago con Stripe
        try:
            stripe_client = StripeClient()
            
            # Crear una intención de pago en Stripe
            currency = pago.moneda.lower()
            description = f"Pago de inscripción para {pago.inscripcion.horario.programa.nombre}"
            
            # Convertir monto a la moneda correcta para Stripe
            amount = pago.monto
            if currency == 'crc':
                # Stripe requiere el monto en céntimos (colones * 100)
                amount_cents = int(amount)
            else:
                # Para USD, convertir a centavos
                amount_cents = int(amount * 100)
            
            # Crear la intención de pago
            payment_intent = stripe_client.create_payment_intent(
                amount=amount,
                currency=currency,
                description=description
            )
            
            # Actualizar el estado del pago
            pago.estado = 'SUCCESS'
            pago.referencia_transaccion = payment_intent['id']
            pago.save()
            
            # Generar notificación para el frontend
            notifier = PaymentNotifier()
            notification = notifier.send_payment_confirmation({
                'id': pago.id,
                'monto': str(pago.monto),
                'moneda': pago.moneda,
                'fecha_pago': pago.fecha_pago
            })
            
            return Response({
                'message': 'Pago procesado exitosamente',
                'payment_intent_id': payment_intent['id'],
                'client_secret': payment_intent['client_secret'],
                'notification': notification
            }, status=status.HTTP_200_OK)
            
        except StripeError as e:
            # Actualizar el estado del pago a fallido
            pago.estado = 'FAILED'
            pago.save()
            
            # Generar notificación de error para el frontend
            notifier = PaymentNotifier()
            notification = notifier.send_payment_failed({
                'id': pago.id,
                'monto': str(pago.monto),
                'moneda': pago.moneda,
                'fecha_pago': pago.fecha_pago
            })
            
            return Response({
                'error': str(e),
                'notification': notification
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Actualizar el estado del pago a fallido
            pago.estado = 'FAILED'
            pago.save()
            
            # Generar notificación de error para el frontend
            notifier = PaymentNotifier()
            notification = notifier.send_payment_failed({
                'id': pago.id,
                'monto': str(pago.monto),
                'moneda': pago.moneda,
                'fecha_pago': pago.fecha_pago
            })
            
            return Response({
                'error': f'Error al procesar el pago: {str(e)}',
                'notification': notification
            }, status=status.HTTP_400_BAD_REQUEST)

# Vista administrativa para Pagos
class AdminPagoViewSet(viewsets.ModelViewSet):
    """Vista administrativa para gestionar pagos a través de la API.
    
    Proporciona funcionalidades CRUD completas con filtrado, búsqueda y ordenamiento.
    """
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['estado', 'metodo_pago', 'moneda']
    search_fields = ['referencia_transaccion']
    ordering_fields = ['fecha_pago', 'monto']
    ordering = ['-fecha_pago']

# Vista administrativa para Pagos de Inscripción
class AdminPagoInscripcionViewSet(viewsets.ModelViewSet):
    """Vista administrativa para gestionar pagos de inscripción a través de la API.
    
    Proporciona funcionalidades CRUD completas con filtrado, búsqueda y ordenamiento.
    """
    queryset = PagoInscripcion.objects.all()
    serializer_class = PagoInscripcionSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['estado', 'metodo_pago', 'moneda']
    search_fields = ['referencia_transaccion', 'inscripcion__usuario__email']
    ordering_fields = ['fecha_pago', 'monto']
    ordering = ['-fecha_pago']

# Vista administrativa para Donaciones
class AdminDonacionViewSet(viewsets.ModelViewSet):
    """Vista administrativa para gestionar donaciones a través de la API.
    
    Proporciona funcionalidades CRUD completas con filtrado, búsqueda y ordenamiento.
    """
    queryset = Donacion.objects.all()
    serializer_class = DonacionSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['estado', 'metodo_pago', 'moneda']
    search_fields = ['nombre_donante', 'email_donante', 'referencia_transaccion']
    ordering_fields = ['fecha_creacion', 'monto']
    ordering = ['-fecha_creacion']

    def get_queryset(self):
        """Filtra los pagos según el tipo de usuario"""
        if self.request.user.is_staff:
            return PagoInscripcion.objects.all()
        return PagoInscripcion.objects.filter(inscripcion__usuario=self.request.user)

    def get_permissions(self):
        """Define permisos según la acción"""
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

class DonacionViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar donaciones al parque
    
    Endpoints principales:
    - GET /donaciones/ - Lista donaciones (filtradas por usuario)
    - POST /donaciones/ - Registra nueva donación (público)
    - GET /donaciones/{id}/ - Ver detalles de donación
    - PUT /donaciones/{id}/ - Actualizar donación (admin)
    - DELETE /donaciones/{id}/ - Eliminar donación (admin)
    - POST /donaciones/{id}/procesar_donacion/ - Procesa la donación
    - POST /donaciones/{id}/procesar_pago/ - Procesa el pago con Stripe
    
    Características especiales:
    - Creación de donaciones sin autenticación
    - Conversión automática de montos entre CRC y USD
    - Seguimiento por email del donante
    
    Ejemplo de uso:
    ```python
    # Registrar donación
    POST /api/donaciones/
    {
        "monto": 100,
        "moneda": "USD",
        "nombre_donante": "Juan Pérez",
        "email_donante": "juan@ejemplo.com",
        "metodo_pago": "TARJETA"
    }
    
    # Procesar donación (admin)
    POST /api/donaciones/1/procesar_donacion/
    
    # Procesar pago con Stripe
    POST /api/donaciones/1/procesar_pago/
    ```
    """
    queryset = Donacion.objects.all()
    serializer_class = DonacionSerializer

    def get_queryset(self):
        """Filtra las donaciones según el tipo de usuario"""
        if self.request.user.is_staff:
            return Donacion.objects.all()
        # For regular users, filter by email if authenticated
        if self.request.user.is_authenticated:
            return Donacion.objects.filter(
                email_donante=self.request.user.email
            )
        # For unauthenticated requests to list, return empty queryset
        return Donacion.objects.none()

    def get_permissions(self):
        """Define permisos según la acción"""
        if self.action == 'create':
            # Donations can be created without authentication
            self.permission_classes = []
        elif self.action in ['update', 'partial_update', 'destroy']:
            # Only admin can update/delete
            self.permission_classes = [IsAdminUser]
        elif self.action == 'procesar_pago':
            # Processing payment doesn't require authentication
            self.permission_classes = []
        else:
            # All other actions require authentication
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_object(self):
        """Override to allow access to donation for procesar_pago without authentication filtering"""
        if self.action == 'procesar_pago':
            # For procesar_pago, bypass the queryset filtering
            return Donacion.objects.get(pk=self.kwargs.get('pk'))
        return super().get_object()

    @action(detail=True, methods=['post'])
    def procesar_donacion(self, request, pk=None):
        """Procesa una donación
        
        Actualiza el estado de la donación según el resultado del procesamiento.
        """
        donacion = self.get_object()
        
        # Aquí iría la lógica de procesamiento de la donación
        # Por ahora, simulamos un proceso exitoso
        try:
            donacion.estado = 'SUCCESS'
            donacion.save()
            return Response({
                'message': 'Donación procesada exitosamente'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], permission_classes=[])
    def procesar_pago(self, request, pk=None):
        """Procesa una donación utilizando Stripe
        
        Actualiza el estado de la donación según el resultado del procesamiento con Stripe.
        """
        # For procesar_pago, we need to get the object without filtering
        try:
            donacion = Donacion.objects.get(pk=pk)
        except Donacion.DoesNotExist:
            return Response({
                'error': 'Donación no encontrada'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Solo procesar donaciones que estén en estado pendiente
        if donacion.estado != 'PENDING':
            return Response({
                'error': 'Esta donación ya ha sido procesada'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Procesar pago con Stripe
        try:
            stripe_client = StripeClient()
            
            # Crear una intención de pago en Stripe
            currency = donacion.moneda.lower()
            description = f"Donación de {donacion.nombre_donante or 'Anónimo'}"
            
            # Convertir monto a la moneda correcta para Stripe
            amount = donacion.monto
            if currency == 'crc':
                # Stripe requiere el monto en céntimos (colones * 100)
                amount_cents = int(amount)
            else:
                # Para USD, convertir a centavos
                amount_cents = int(amount * 100)
            
            # Crear la intención de pago
            payment_intent = stripe_client.create_payment_intent(
                amount=amount,
                currency=currency,
                description=description
            )
            
            # Actualizar el estado de la donación
            donacion.estado = 'SUCCESS'
            donacion.referencia_transaccion = payment_intent['id']
            donacion.save()
            
            # Generar notificación para el frontend
            notifier = PaymentNotifier()
            notification = notifier.send_payment_confirmation({
                'id': donacion.id,
                'monto': str(donacion.monto),
                'moneda': donacion.moneda,
                'fecha_pago': donacion.fecha_creacion
            })
            
            return Response({
                'message': 'Donación procesada exitosamente',
                'payment_intent_id': payment_intent['id'],
                'client_secret': payment_intent['client_secret'],
                'notification': notification
            }, status=status.HTTP_200_OK)
            
        except StripeError as e:
            # Actualizar el estado de la donación a fallido
            donacion.estado = 'FAILED'
            donacion.save()
            
            # Generar notificación de error para el frontend
            notifier = PaymentNotifier()
            notification = notifier.send_payment_failed({
                'id': donacion.id,
                'monto': str(donacion.monto),
                'moneda': donacion.moneda,
                'fecha_pago': donacion.fecha_creacion
            })
            
            return Response({
                'error': str(e),
                'notification': notification
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Actualizar el estado de la donación a fallido
            donacion.estado = 'FAILED'
            donacion.save()
            
            # Generar notificación de error para el frontend
            notifier = PaymentNotifier()
            notification = notifier.send_payment_failed({
                'id': donacion.id,
                'monto': str(donacion.monto),
                'moneda': donacion.moneda,
                'fecha_pago': donacion.fecha_creacion
            })
            
            return Response({
                'error': f'Error al procesar la donación: {str(e)}',
                'notification': notification
            }, status=status.HTTP_400_BAD_REQUEST)

class MetodosPagoView(APIView):
    """Vista para obtener los métodos de pago disponibles
    
    Endpoint:
    - GET /metodos-pago/ - Obtiene lista de métodos de pago
    
    Retorna:
    Lista de diccionarios con:
    - id: Identificador del método de pago
    - nombre: Nombre descriptivo del método
    
    Métodos disponibles:
    - Tarjeta de Crédito/Débito (CARD)
    - PayPal (PAYPAL)
    - Efectivo/SINPE (CASH)
    - Transferencia Bancaria (TRANSFER)
    
    Ejemplo de uso:
    ```python
    # Obtener métodos de pago
    GET /api/metodos-pago/
    
    # Respuesta
    [
        {"id": "CARD", "nombre": "Tarjeta de Crédito/Débito"},
        {"id": "PAYPAL", "nombre": "PayPal"},
        ...
    ]
    ```
    """
    def get(self, request):
        """Retorna la lista de métodos de pago disponibles"""
        metodos = [
            {'id': 'CARD', 'nombre': 'Tarjeta de Crédito/Débito'},
            {'id': 'PAYPAL', 'nombre': 'PayPal'},
            {'id': 'CASH', 'nombre': 'Efectivo/SINPE'},
            {'id': 'TRANSFER', 'nombre': 'Transferencia Bancaria'}
        ]
        return Response(metodos)

@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(APIView):
    """View para manejar webhooks de Stripe
    
    Esta vista recibe eventos de Stripe y actualiza los estados de los pagos
    en consecuencia.
    """
    permission_classes = []  # No requiere autenticación
    
    def post(self, request):
        """Maneja eventos de webhook de Stripe"""
        try:
            stripe_client = StripeClient()
            payload = request.body
            sig_header = request.META['HTTP_STRIPE_SIGNATURE']
            event = None

            try:
                event = stripe.Webhook.construct_event(
                    payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
                )
            except ValueError:
                # Payload inválido
                return HttpResponse(status=400)
            except stripe.error.SignatureVerificationError:
                # Firma inválida
                return HttpResponse(status=400)

            # Manejar el evento
            if event['type'] == 'payment_intent.succeeded':
                payment_intent = event['data']['object']
                # Actualizar el estado del pago en nuestra base de datos
                try:
                    pago = Pago.objects.get(referencia_transaccion=payment_intent['id'])
                    pago.estado = 'SUCCESS'
                    pago.save()
                except Pago.DoesNotExist:
                    try:
                        pago_inscripcion = PagoInscripcion.objects.get(referencia_transaccion=payment_intent['id'])
                        pago_inscripcion.estado = 'SUCCESS'
                        pago_inscripcion.save()
                    except PagoInscripcion.DoesNotExist:
                        try:
                            donacion = Donacion.objects.get(referencia_transaccion=payment_intent['id'])
                            donacion.estado = 'SUCCESS'
                            donacion.save()
                        except Donacion.DoesNotExist:
                            pass  # Pago no encontrado en nuestra base de datos

            elif event['type'] == 'payment_intent.payment_failed':
                payment_intent = event['data']['object']
                # Actualizar el estado del pago en nuestra base de datos
                try:
                    pago = Pago.objects.get(referencia_transaccion=payment_intent['id'])
                    pago.estado = 'FAILED'
                    pago.save()
                except Pago.DoesNotExist:
                    try:
                        pago_inscripcion = PagoInscripcion.objects.get(referencia_transaccion=payment_intent['id'])
                        pago_inscripcion.estado = 'FAILED'
                        pago_inscripcion.save()
                    except PagoInscripcion.DoesNotExist:
                        try:
                            donacion = Donacion.objects.get(referencia_transaccion=payment_intent['id'])
                            donacion.estado = 'FAILED'
                            donacion.save()
                        except Donacion.DoesNotExist:
                            pass  # Pago no encontrado en nuestra base de datos

            return HttpResponse(status=200)
        except Exception as e:
            return HttpResponse(status=500)
