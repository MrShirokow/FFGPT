from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView

from .models import User


class UserProfileView(LoginRequiredMixin, UpdateView):
    """View to display and edit the user details."""

    model = User
    fields = (
        "avatar",
        "first_name",
        "last_name",
    )
    template_name = "users/profile.html"
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None) -> AbstractBaseUser | AnonymousUser:
        """Get the user object from the request.

        This is overridden because the user profile page is accessible via
        the URL `/user/profile/` without a primary key.

        """
        return self.request.user


class UserPasswordChangeView(PasswordChangeView):
    """View to change the user's password."""

    form_class = PasswordChangeForm
    template_name = "users/change_password.html"
    success_url = reverse_lazy("profile")
