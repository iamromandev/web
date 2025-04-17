from django.urls import path

from .api import RegistrationApi

urlpatterns = [
    path("api/register", RegistrationApi.as_view(), name="register"),
]
