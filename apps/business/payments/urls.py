from django.urls import path
from apps.business.payments.views import (
    PagoViewSet, PagoInscripcionViewSet, DonacionViewSet, MetodosPagoView,
    AdminPagoViewSet, AdminPagoInscripcionViewSet, AdminDonacionViewSet,
    StripeWebhookView
)

# Configuración de las rutas para la API de Payments (Pagos)
# Cada ruta proporciona endpoints para operaciones CRUD en diferentes modelos

app_name = 'payments'

urlpatterns = [
    # Pagos - Gestión de pagos generales
    path('pagos/', PagoViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='pagos-list-create'),
    
    path('pagos/<int:pk>/', PagoViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='pagos-detail'),

    # Pagos de Inscripción - Gestión de pagos de inscripciones
    path('pagos-inscripcion/', PagoInscripcionViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='pagos-inscripcion-list-create'),
    
    path('pagos-inscripcion/<int:pk>/', PagoInscripcionViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='pagos-inscripcion-detail'),

    # Donaciones - Gestión de donaciones al parque
    path('donaciones/', DonacionViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='donaciones-list-create'),
    
    path('donaciones/<int:pk>/', DonacionViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='donaciones-detail'),

    # Administración de Pagos - Gestión administrativa de pagos
    path('admin/pagos/', AdminPagoViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='admin-pagos-list-create'),
    
    path('admin/pagos/<int:pk>/', AdminPagoViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='admin-pagos-detail'),

    # Administración de Pagos de Inscripción - Gestión administrativa de pagos de inscripciones
    path('admin/pagos-inscripcion/', AdminPagoInscripcionViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='admin-pagos-inscripcion-list-create'),
    
    path('admin/pagos-inscripcion/<int:pk>/', AdminPagoInscripcionViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='admin-pagos-inscripcion-detail'),

    # Administración de Donaciones - Gestión administrativa de donaciones
    path('admin/donaciones/', AdminDonacionViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='admin-donaciones-list-create'),
    
    path('admin/donaciones/<int:pk>/', AdminDonacionViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='admin-donaciones-detail'),

    # Webhook de Stripe - Para recibir eventos de pago
    path('stripe/webhook/', StripeWebhookView.as_view(), name='stripe-webhook'),

    # Métodos de Pago - Vista para obtener métodos de pago disponibles
    path('metodos-pago/', MetodosPagoView.as_view(), name='metodos-pago'),
]