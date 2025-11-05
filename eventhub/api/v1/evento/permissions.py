from rest_framework import permissions

class IsOrganizerOrReadOnly(permissions.BasePermission):
    """
    Permite el acceso de lectura a cualquiera, pero solo el organizador del evento
    puede realizar actualizaciones o eliminaciones.
    """

    def has_object_permission(self, request, view, obj):
        # GET, HEAD, OPTIONS son siempre permitidos (lectura)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Para métodos de escritura (POST, PUT, PATCH, DELETE),
        # solo el organizador del evento tiene permiso.
        return obj.organizador == request.user