"""
===========================================
 CONFIGURACIÓN DE DESARROLLO DEL BACKEND DJANGO
 Archivo: config/settings/development.py
===========================================
"""

from .base import *

# ==============================
# CONFIGURACIÓN DE DESARROLLO
# ==============================

# Debug activado para desarrollo
DEBUG = True

# Hosts permitidos en desarrollo
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '[::1]',  # IPv6 localhost
]

# Configuración de base de datos para desarrollo
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Configuración de correo para desarrollo (consola)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Configuración de logging para desarrollo
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

print("🔧 Configuración de desarrollo cargada")