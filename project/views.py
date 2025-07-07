from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from authentication.models import User
from .permissions import IsAuthorOrReadOnly, IsContributor


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        return Project.objects.filter(contributors__user=self.request.user).distinct()

    def perform_create(self, serializer):
        serializer.save(author_user=self.request.user)


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
        """Gère PATCH /issues/<id>/"""
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Gère DELETE /issues/<id>/"""
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
        serializer.save(issue=issue, author_user=self.request.user)

    def update(self, request, *args, **kwargs):
        """Gère PUT /comments/<id>/"""
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """Gère PATCH /comments/<id>/"""
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Gère DELETE /comments/<id>/"""
        return super().destroy(request, *args, **kwargs)
