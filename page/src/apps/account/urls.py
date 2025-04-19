from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

from .views import LoginView, ProtectedView, RegistrationView, VerifyEmailView

urlpatterns = [
    path("api/register/", RegistrationView.as_view(), name="register"),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path(
        'api/verify-email/<str:uidb64>/<str:token>/',
        VerifyEmailView.as_view(), name='verify_email'
    ),
    path("api/protected/", ProtectedView.as_view(), name="protected"),
]
