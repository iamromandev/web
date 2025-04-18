from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

from .api import LoginView, RegistrationApi
from .views import ProtectedView

urlpatterns = [
    path("api/register/", RegistrationApi.as_view(), name="register"),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path("api/protected/", ProtectedView.as_view(), name="protected"),
]
