from rest_framework import viewsets, permissions
from django.shortcuts import get_object_or_404
from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly, IsContributor
from rest_framework.exceptions import PermissionDenied


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        return Project.objects.filter(contributors__user=self.request.user).distinct()

    def perform_create(self, serializer):
        serializer.save(author_user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()
        if project.author_user != request.user:
            raise PermissionDenied("Seul l'auteur peut supprimer ce projet.")
        return super().destroy(request, *args, **kwargs)


class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated, IsContributor, IsAuthorOrReadOnly]

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        return Contributor.objects.filter(project__id=project_id)

    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_id')
        project = get_object_or_404(Project, pk=project_id)
        serializer.save(project=project, author_user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """
        Supprimer un contributeur si l'utilisateur connecté est l'auteur du projet.
        """
        contributor = self.get_object()
        project = contributor.project

        # Seul l'auteur du projet peut supprimer un contributeur
        if project.author_user != request.user:
            raise PermissionDenied("Seul l'auteur du projet peut supprimer un contributeur.")

        return super().destroy(request, *args, **kwargs)


class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated, IsContributor, IsAuthorOrReadOnly]

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        return Issue.objects.select_related("project", "author_user", "assignee_user").filter(project__id=project_id)

    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_id')
        project = get_object_or_404(Project, pk=project_id)
        serializer.save(project=project, author_user=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        issue = self.get_object()  # récupère Issue(id=i)
        if issue.author_user != request.user:
            raise PermissionDenied("Seul l'auteur peut modifier cette issue.")
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        issue = self.get_object()
        if issue.author_user != request.user:
            raise PermissionDenied("Seul l'auteur peut supprimer cette issue.")
        return super().destroy(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsContributor, IsAuthorOrReadOnly]

    def get_queryset(self):
        issue_id = self.kwargs.get('issue_id')
        return Comment.objects.select_related("issue", "author_user").filter(issue__id=issue_id)

    def perform_create(self, serializer):
        issue_id = self.kwargs.get('issue_id')
        issue = get_object_or_404(Issue, pk=issue_id)

        # Vérifie si l'utilisateur a déjà commenté cette issue
        already_exists = Comment.objects.filter(issue=issue, author_user=self.request.user).exists()
        if already_exists:
            raise PermissionDenied("Vous avez déjà posté un commentaire sur cette issue.")

        serializer.save(issue=issue, author_user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """Gère DELETE /comments/<id>/ – Seul l'auteur peut supprimer"""
        comment = self.get_object()
        if comment.author_user != request.user:
            raise PermissionDenied("Seul l'auteur peut supprimer ce commentaire.")
        return super().destroy(request, *args, **kwargs)
