from rest_framework.permissions import BasePermission, IsAuthenticated

class IsAuthenticatedAndRole(BasePermission):
    """
    Permite acceso solo a usuarios autenticados y, opcionalmente, usuarios con un rol específico (grupo).
    Uso: establecer el atributo 'required_role' en la clase de vista para restringir a un nombre de grupo.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        required_role = getattr(view, 'required_role', None)
        if required_role is None:
            return True  # Solo requiere autenticación
        return request.user.groups.filter(name=required_role).exists()

class IsAuthenticatedOrReadOnly(BasePermission):
    """
    Permite acceso de solo lectura a usuarios anónimos y acceso completo a usuarios autenticados.
    Para operaciones de escritura (POST, PUT, PATCH, DELETE), se requiere autenticación.
    Opcionalmente, puede restringir operaciones de escritura a usuarios con un rol específico.
    """
    def has_permission(self, request, view):
        # Permite acceso de solo lectura para métodos seguros (GET, HEAD, OPTIONS)
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        # Para métodos de escritura, requiere autenticación
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Verifica el requerimiento de rol específico en operaciones de escritura
        required_role = getattr(view, 'required_role', None)
        if required_role is None:
            return True  # Solo requiere autenticación
        return request.user.groups.filter(name=required_role).exists()
