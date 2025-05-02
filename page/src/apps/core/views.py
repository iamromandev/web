from rest_framework import generics, permissions, status
from rest_framework_simplejwt.authentication import JWTAuthentication

from .mixins import InjectCoreMixin
from .models import User
from .serializers import UserRetrieveSerializer


class SelfUserRetrieveView(InjectCoreMixin, generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = UserRetrieveSerializer
    queryset = None
    lookup_field = None

    def get_object(self) -> User:
        return self.request.user
