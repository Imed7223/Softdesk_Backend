from rest_framework import permissions


class IsSelf(permissions.BasePermission):
    """
    L'utilisateur ne peut voir ou modifier que ses propres données.
    """
    def has_object_permission(self, request, view, obj):
        # Autoriser toutes les requêtes de lecture si l'utilisateur est authentifié
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user
