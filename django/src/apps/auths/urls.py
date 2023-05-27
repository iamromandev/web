from django.urls import path, include

from .views import SignUpView

urlpatterns = [
    path("", include("rest_framework.urls", namespace="rest-framework")),
    # path("signup/", SignUpView.as_view(), name="signup"),
]
