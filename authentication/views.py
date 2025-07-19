from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from authentication.serializers import UserSerializer

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
