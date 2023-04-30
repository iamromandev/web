from django.contrib.auth.forms import UserCreationForm

from apps.core.models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]
