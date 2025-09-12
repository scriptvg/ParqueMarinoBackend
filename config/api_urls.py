from django.urls import path, include

urlpatterns = [
    path('api/infrastructure/', include('infrastructure.urls')),
    path('api/wildlife/', include('wildlife.urls')),  # Rutas para la gestión de vida silvestre
    path('api/education/', include('education.urls')),  # Rutas para la gestión de servicios educativos
    path('api/tickets/', include('tickets.urls')),  # Rutas para la gestión de tickets y visitas
    path('api/payments/', include('payments.urls')),
    # URLs de auditoría
    path('api/audit/', include('audit.urls')),  # Rutas para la gestión de pagos y donaciones
    path('api/exhibitions/', include('exhibitions.urls')),  # Rutas para la gestión de exhibiciones
    path('api/documents/', include('documents.urls')),  # Rutas para la gestión de documentos
]
