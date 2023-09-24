from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView as LV
from django.urls import reverse_lazy

from .forms import (
    RegistrationForm,
    LoginForm,
)


# Create your views here.
class RegistrationView(CreateView):
    form_class = RegistrationForm
    success_url = reverse_lazy("login")
    template_name = "auths/registration.html"


class LoginView(LV):
    form_class = LoginForm
    template_name = "auths/login.html"
