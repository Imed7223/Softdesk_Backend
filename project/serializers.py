from rest_framework import serializers
from .models import Project, Contributor, Issue, Comment


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author_user', 'created_time']
        extra_kwargs = {
            'author_user': {'required': False, 'allow_null': True}
        }   

class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project', 'permission', 'role']


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'issue', 'author_user', 'description', 'uuid', 'created_time']
        extra_kwargs = {
            'author_user': {'read_only': True},
            'uuid': {'read_only': True},
            'created_time': {'read_only': True},
        }
