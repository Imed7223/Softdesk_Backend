from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Project, Contributor
from .serializers import ProjectSerializer, ContributorSerializer


class IsAuthorContributor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Project):
            return (
                obj.author_user == request.user or
                Contributor.objects.filter(project=obj, user=request.user).exists()
            )
        return False
 
class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Project.objects.filter(contributors__user=self.request.user).distinct()
        return Project.objects.all()

    def perform_create(self, serializer):
        project = serializer.save(author_user=self.request.user)
        Contributor.objects.create(user=self.request.user, project=project, role='Author', permission='AUTHOR')

class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Contributor.objects.filter(user=user)
        return Contributor.objects.none()

