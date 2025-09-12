"""
===========================================
 CONFIGURACIÓN PRINCIPAL DEL BACKEND DJANGO
 Archivo: settings.py
===========================================
"""

# Este archivo ahora actúa como un alias para la nueva estructura modular
# Para usar la nueva configuración, establezca DJANGO_SETTINGS_MODULE en:
# - config.settings.development (para desarrollo)
# - config.settings.production (para producción)

# Mantenemos el archivo original para compatibilidad con la configuración existente
from .settings.base import *

print("⚠️  Usando configuración heredada. Considere usar config.settings.development o config.settings.production")

# ==============================
# IMPORTACIONES NECESARIAS
# ==============================
from pathlib import Path        # Manejo seguro de rutas
from datetime import timedelta  # Manejo de tiempos (JWT, sesiones, etc.)
import os                       # Variables de entorno y rutas
from dotenv import load_dotenv  # Cargar variables desde archivo .env

# Cargar variables de entorno
load_dotenv()


# ==============================
# BASE DEL PROYECTO
# ==============================
BASE_DIR = Path(__file__).resolve().parent.parent


# ==============================
# CONFIGURACIÓN DE SEGURIDAD
# ==============================
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')  # No exponer en repos públicos
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',')  # Lista separada por comas


# ==============================
# CONFIGURACIÓN DE CORS
# ==============================
CORS_ALLOW_CREDENTIALS = os.environ.get('DJANGO_CORS_ALLOW_CREDENTIALS', 'False') == 'True'
CORS_ALLOWED_ORIGINS = [
  "http://localhost:5173",
  "http://127.0.0.1:5173"
]
CORS_ALLOWED_METHODS = os.environ.get('DJANGO_CORS_ALLOWED_METHODS', '').split(',')
CORS_ALLOWED_HEADERS = os.environ.get('DJANGO_CORS_ALLOWED_HEADERS', '').split(',')


# ==============================
# APLICACIONES INSTALADAS
# ==============================
INSTALLED_APPS = [
    # Aplicación de auditoría
    'audit',
    # Django core apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Terceros
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',
    'rest_framework.authtoken',
    'rest_framework_simplejwt.token_blacklist',
    'drf_spectacular',
    'drf_yasg',
    'storages',  # AWS S3
    'boto3',
    

    # Local apps
    
    'security',
    'infrastructure',
    'exhibitions',
    'wildlife',
    'education',
    'payments',
    'tickets',  # Sistema de tickets y visitas
    'documents',
]


# ==============================
# MIDDLEWARE
# ==============================
MIDDLEWARE = [
    # Middleware de auditoría
    'audit.middleware.AuditLogMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ==============================
# CONFIGURACIÓN DE URLS Y WSGI
# ==============================
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'


# ==============================
# TEMPLATES
# ==============================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Carpetas adicionales de templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ==============================
# BASE DE DATOS
# ==============================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Cambiar en producción
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ==============================
# CONFIGURACIÓN DE DRF Y JWT
# ==============================
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_ENABLED": False,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
    "TOKEN_OBTAIN_SERIALIZER": "api.serializers.CustomTokenObtainPairSerializer",
    "EMAIL_FIELD": "email",
}


# ==============================
# VALIDACIÓN DE CONTRASEÑAS
# ==============================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
]


# ==============================
# INTERNACIONALIZACIÓN
# ==============================
LANGUAGE_CODE = 'es-cr'
TIME_ZONE = 'America/Costa_Rica'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

# ==============================
# CONFIGURACIÓN AWS S3
# ==============================
USE_S3 = os.environ.get('USE_S3', 'False') == 'True'

if USE_S3:
    # Configuración AWS
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_DEFAULT_ACL = None
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    
    
    # Configuración de almacenamiento

    DEFAULT_FILE_STORAGE = 'config.storage_backends.MediaStorage'
    
    # URLs para archivos estáticos y media

    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
else:
    # Configuración local
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'


# ==============================
# CLAVE PRIMARIA POR DEFECTO
# ==============================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==============================
# CONFIGURACIÓN DE STRIPE
# ==============================
STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')

# ==============================
# CONFIGURACIÓN DE EMAIL
# ==============================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@parquemarino.com')
EMAIL_REPLY_TO = [os.environ.get('EMAIL_REPLY_TO', 'support@parquemarino.com')]

SITE_NAME = 'Parque Marino'
CONTACT_EMAIL = 'info@parquemarino.com'
SUPPORT_PHONE = '+506 XXXX XXXX'
