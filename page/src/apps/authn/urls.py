from django.urls import path
from rest_framework_simplejwt.views import (
    TokenVerifyView,
)

from .views import (
    LoginView,
    ProtectedView,
    RegistrationView,
    TokenRefreshView,
    TokenView,
    VerifyEmailView,
)

urlpatterns = [
    path("auth/register/", RegistrationView.as_view(), name="register"),
    path(
        'auth/verify-email/<str:pkb64>/<str:token>/',
        VerifyEmailView.as_view(), name='verify_email'
    ),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/token/', TokenView.as_view(), name='token'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path("auth/protected/", ProtectedView.as_view(), name="protected"),
]
