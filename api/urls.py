"""
Main API URLs for Parque Marino Backend
"""

from django.urls import path, include

app_name = 'api'

urlpatterns = [
    # Version 1 of the API
    path('v1/', include('api.v1.urls', namespace='v1')),
    
    # Default to v1 for backward compatibility
    path('', include('api.v1.urls')),
]