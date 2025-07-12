from rest_framework import serializers
from .models import Project, Contributor, Issue, Comment


class ProjectSerializer(serializers.ModelSerializer):
    author_user = serializers.ReadOnlyField(source='author_user.username')

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author_user', 'created_time']
        extra_kwargs = {
            'author_user': {'required': False, 'allow_null': True}
        }


class ContributorSerializer(serializers.ModelSerializer):
    author_user = serializers.ReadOnlyField(source='author_user.username')

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project', 'permission', 'role', 'author_user']


class IssueSerializer(serializers.ModelSerializer):
    author_user = serializers.ReadOnlyField(source='author_user.username')

    class Meta:
        model = Issue
        fields = [
            'id', 'title', 'description', 'tag', 'priority', 'status',
            'project', 'author_user', 'assignee_user', 'created_time'
        ]
        read_only_fields = ['author_user', 'created_time']


class CommentSerializer(serializers.ModelSerializer):
    author_user = serializers.ReadOnlyField(source='author_user.username')

    class Meta:
        model = Comment
        fields = ['id', 'issue', 'author_user', 'description', 'uuid', 'created_time']
        read_only_fields = ['author_user', 'uuid', 'created_time']
