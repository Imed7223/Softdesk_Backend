from rest_framework import permissions
from project.models import Contributor


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Autorise uniquement l'auteur à modifier ou supprimer l'objet.
    Les autres utilisateurs peuvent seulement lire.
    """

    def has_object_permission(self, request, view, obj):
        # Lecture autorisée à tous les utilisateurs connectés
        if request.method in permissions.SAFE_METHODS:
            return True

        # Modification/suppression autorisée uniquement à l'auteur
        return obj.author_user == request.user


class IsContributor(permissions.BasePermission):
    """
    Autorise uniquement les contributeurs à accéder aux ressources d’un projet.
    """
    def has_permission(self, request, view):
        project_id = view.kwargs.get('project_id') or request.data.get('project')
        if not project_id or not request.user.is_authenticated:
            return False
        return Contributor.objects.filter(project_id=project_id, user=request.user).exists()
