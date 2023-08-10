from django.contrib.auth.forms import UserCreationForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    """Form for creating a new user.

    The custom form is needed because the application uses a custom user.

    """

    class Meta:
        model = User
        fields = ("email", "password1", "password2")
