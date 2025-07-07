from django.shortcuts import render
from rest_framework import viewsets, permissions
from authentication.models import User
from authentication.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
