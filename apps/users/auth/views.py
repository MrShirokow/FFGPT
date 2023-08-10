from django.contrib.auth import login
from django.forms import BaseModelForm
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
)
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from ..forms import CustomUserCreationForm

ViewResponse = (
    HttpResponseRedirect | HttpResponsePermanentRedirect | HttpResponse
)


class UserSignUpView(CreateView):
    """Class-based view for creating a new user."""

    form_class = CustomUserCreationForm
    success_url = reverse_lazy("fanfiction-list")
    template_name = "users/auth/signup.html"

    def get(self, request: HttpRequest, *args, **kwargs) -> ViewResponse:
        """Return page with the user registration form.

        If user is authenticated then redirect to home page with fanfictions.

        """
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return render(request, self.template_name)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Login new user after registration if form data is valid."""
        view_response = super().form_valid(form)
        user = self.object
        login(self.request, user)
        return view_response
