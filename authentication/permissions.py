from rest_framework import permissions


class IsSelf(permissions.BasePermission):
    """
    L'utilisateur ne peut voir ou modifier que ses propres données.
    """
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsAdminOrEmptyList(permissions.BasePermission):
    """
    Autorise uniquement le superuser à voir la liste des utilisateurs.
    """
    def has_permission(self, request, view):
        return request.method != 'GET' or request.user.is_superuser
