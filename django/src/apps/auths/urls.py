from django.urls import path, include

from rest_framework.authtoken import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import SignUpView

urlpatterns = [
    # path("", include("rest_framework.urls", namespace="rest-framework")),
    # path("", include("django.contrib.auth.urls")),
    # path("token/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    # path("token/refresh", TokenRefreshView.as_view(), name="token-refresh"),
    # path("auth-token/", views.obtain_auth_token),
    # path("", include("dj_rest_auth.urls")),
    # path("registration/", include("dj_rest_auth.registration.urls")),
    # path("signup/", SignUpView.as_view(), name="signup"),
]
