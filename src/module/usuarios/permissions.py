from rest_framework import permissions

class IsDocente(permissions.BasePermission):
    """
    Permite acceso solo a usuarios que son docentes.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'docente')

class IsAlumno(permissions.BasePermission):
    """
    Permite acceso solo a usuarios que son alumnos.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'alumno')

class IsDocenteOrAlumno(permissions.BasePermission):
    """
    Permite acceso a usuarios que son docentes o alumnos.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (hasattr(request.user, 'docente') or hasattr(request.user, 'alumno'))

class IsDocenteOrReadOnly(permissions.BasePermission):
    """
    Permite acceso de escritura solo a docentes, pero lectura a todos los usuarios autenticados.
    """
    def has_permission(self, request, view):
        # Permitir GET, HEAD, OPTIONS a cualquier usuario autenticado
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        # Permitir escritura solo a docentes
        return request.user.is_authenticated and hasattr(request.user, 'docente')
