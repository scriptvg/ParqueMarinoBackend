"""
===========================================
 CONFIGURACIÓN DEL BACKEND DJANGO
 Archivo: config/settings/__init__.py
===========================================
"""

import os

# Determinar qué configuración cargar basado en la variable de entorno
DJANGO_SETTINGS_MODULE = os.environ.get('DJANGO_SETTINGS_MODULE', 'config.settings.development')

if DJANGO_SETTINGS_MODULE == 'config.settings.production':
    from .production import *
elif DJANGO_SETTINGS_MODULE == 'config.settings.development':
    from .development import *
else:
    from .base import *