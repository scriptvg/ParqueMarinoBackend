"""
API URLs for Parque Marino Backend v1
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import routers

# API v1 URLs
app_name = 'api_v1'

urlpatterns = [
    # Include router URLs
    path('', include(routers.router.urls)),
    
    # Wildlife module
    path('wildlife/', include('apps.business.wildlife.urls')),
    
    # Exhibitions module
    path('exhibitions/', include('apps.business.exhibitions.urls')),
    
    # Education module
    path('education/', include('apps.business.education.urls')),
    
    # Payments module
    path('payments/', include('apps.business.payments.urls')),
    
    # Tickets module
    path('tickets/', include('apps.business.tickets.urls')),
    
    # Infrastructure module
    path('infrastructure/', include('apps.business.infrastructure.urls')),
    
    # Documents module
    path('documents/', include('apps.business.documents.urls')),
    
    # Audit module
    path('audit/', include('apps.support.audit.urls')),
    
    # Security module
    path('auth/', include('apps.support.security.urls')),
    
    # Messaging module
    path('messaging/', include('apps.support.messaging.urls')),
]