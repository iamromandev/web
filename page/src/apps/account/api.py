from rest_framework import generics, permissions, status
from rest_framework.response import Response

from apps.core.models import User

from .serializers import RegistrationSerializer
from .services.auth_service import AuthService


class RegistrationApi(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            data = AuthService.register(**serializer.validated_data)
            return Response(
                data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
