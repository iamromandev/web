from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

from .api import LoginApi, ProtectedApi, RegistrationApi, VerifyEmailApi

urlpatterns = [
    path("api/register/", RegistrationApi.as_view(), name="register"),
    path('api/login/', LoginApi.as_view(), name='login'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path(
        'api/verify-email/<str:uidb64>/<str:token>/',
        VerifyEmailApi.as_view(), name='verify_email'
    ),
    path("api/protected/", ProtectedApi.as_view(), name="protected"),
]
