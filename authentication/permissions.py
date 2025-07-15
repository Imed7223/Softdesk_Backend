from rest_framework import permissions


class IsSelf(permissions.BasePermission):
    """
    L'utilisateur ne peut voir ou modifier que ses propres données.
    """
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsAdminOrEmptyList(permissions.BasePermission):
    """
    Autorise la liste complète uniquement pour le superutilisateur.
    """
    def has_permission(self, request, view):
        return True  # Autoriser tout le monde à faire la requête GET
