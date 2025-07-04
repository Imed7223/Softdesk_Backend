from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Project, Contributor
from project.models import Issue, Comment
from project.serializers import  IssueSerializer, CommentSerializer
from authentication.models import User
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
        # On vérifie si l'utilisateur est connecté
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(author_user=user)

    @action(detail=True, methods=['get', 'post'], url_path='issues')
    def issues(self, request, pk=None):
        project = self.get_object()

        if request.method == 'GET':
            issues = project.issues.all()
            serializer = IssueSerializer(issues, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            if not request.user.is_authenticated:
                return Response({"detail": "Authentification requise."}, status=status.HTTP_401_UNAUTHORIZED)

            data = request.data.copy()
            data['project'] = project.id
            data['author_user'] = request.user.id

            serializer = IssueSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(
                {"detail": "Erreur de validation", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

    
    @action(detail=True, methods=['get', 'post'], url_path=r'issues/(?P<issue_id>\d+)/comments')
    def comments(self, request, pk=None, issue_id=None):
        try:
            project = self.get_object()
            issue = project.issues.get(pk=issue_id)
        except Issue.DoesNotExist:
            return Response({"detail": "Issue non trouvée."}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            comments = issue.comments.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            data = request.data.copy()
            data['issue'] = issue.id
            serializer = CommentSerializer(data=data)
            if serializer.is_valid():
                serializer.save(author_user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(
                {"detail": "Erreur de validation", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )


class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user = self.request.user
        return Contributor.objects.all()