from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

from .views import LoginView, ProtectedView, RegistrationView, TokenView, VerifyEmailView

urlpatterns = [
    path("api/register/", RegistrationView.as_view(), name="register"),
    path(
        'api/verify-email/<str:pkb64>/<str:token>/',
        VerifyEmailView.as_view(), name='verify_email'
    ),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/token/', TokenView.as_view(), name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path("api/protected/", ProtectedView.as_view(), name="protected"),
]
