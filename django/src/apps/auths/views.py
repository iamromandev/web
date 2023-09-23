from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .forms import RegistrationForm


# Create your views here.
class RegistrationView(CreateView):
    form_class = RegistrationForm
    success_url = reverse_lazy("login")
    template_name = "auths/registration.html"
