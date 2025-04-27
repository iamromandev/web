from rest_framework import permissions, viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Profile as _Profile
from .serializers import ProfileSerializer as _ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = _ProfileSerializer
    queryset = _Profile.objects.all()
