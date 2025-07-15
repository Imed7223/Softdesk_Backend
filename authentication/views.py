from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from authentication.models import User
from authentication.serializers import UserSerializer
from authentication.permissions import IsSelf, IsAdminOrEmptyList


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet principal pour les utilisateurs.
    - Seul le superuser peut lister tous les utilisateurs.
    - Les utilisateurs peuvent modifier uniquement leur propre profil.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrEmptyList]

    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsSelf()]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        # Seul le superuser voit tous les utilisateurs
        if request.user.is_superuser:
            return super().list(request, *args, **kwargs)
        return Response([])


class MeViewSet(viewsets.ViewSet):
    """
    ViewSet pour l'utilisateur connecté : /api/users/me/
    """
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def update(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request):
        request.user.delete()
        return Response({"detail": "Compte supprimé."}, status=status.HTTP_204_NO_CONTENT)
