import json
from django.contrib.auth import get_user_model
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from .models import AuditLog

User = get_user_model()

class AuditLogMiddleware(MiddlewareMixin):
    """Middleware para registrar automáticamente las solicitudes HTTP.
    
    Este middleware captura todas las solicitudes HTTP y sus respuestas,
    registrándolas en el sistema de auditoría para su posterior análisis.
    """
    
    def process_response(self, request, response):
        """Procesa la respuesta y registra la actividad.
        
        Args:
            request: La solicitud HTTP.
            response: La respuesta HTTP.
            
        Returns:
            response: La respuesta HTTP sin modificar.
        """
        
        # Obtener el usuario autenticado o None
        user = request.user if request.user.is_authenticated else None
        
        # Intentar decodificar el cuerpo de la solicitud
        try:
            request_body = request.body.decode('utf-8')
            try:
                request_body = json.loads(request_body)
            except json.JSONDecodeError:
                pass
        except:
            request_body = None
        
        # Intentar decodificar el cuerpo de la respuesta
        try:
            response_body = response.content.decode('utf-8')
            try:
                response_body = json.loads(response_body)
            except json.JSONDecodeError:
                pass
        except:
            response_body = None
        
        # Crear el registro de auditoría
        AuditLog.objects.create(
            timestamp=timezone.now(),
            user=user,
            action=f'{request.method} {request.path}',
            model='API Request',
            details=f'Request Body: {request_body}, '
                   f'Response Code: {response.status_code}, '
                   f'Response Body: {response_body}'
        )
        
        return response