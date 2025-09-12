from rest_framework import serializers
from .models import AuditLog
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    """Serializador para mostrar información básica del usuario en los registros de auditoría."""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class AuditLogSerializer(serializers.ModelSerializer):
    """Serializador para el modelo AuditLog.
    
    Este serializador maneja la conversión de los registros de auditoría
    a formato JSON y viceversa, incluyendo información detallada del usuario.
    """
    
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = AuditLog
        fields = ['id', 'timestamp', 'user', 'action', 'model', 'record_id', 'details']
        read_only_fields = ['timestamp']