from django.contrib.auth.forms import UserCreationForm

from apps.core.models import User


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]
