from django.urls import path, include

from rest_framework.authtoken import views

from .views import SignUpView

urlpatterns = [
    path("", include("rest_framework.urls", namespace="rest-framework")),
    # path("auth-token/", views.obtain_auth_token),
    path("", include("dj_rest_auth.urls")),
    # path("registration/", include("dj_rest_auth.registration.urls")),
    # path("signup/", SignUpView.as_view(), name="signup"),
]
