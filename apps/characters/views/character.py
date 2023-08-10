from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic

from dal import autocomplete
from django_filters.views import FilterView

from ..filters import CharacterFilter, UserCharacterFilter
from ..forms import CharacterForm
from ..models import Character


class CharacterDetailView(LoginRequiredMixin, generic.DetailView):
    """Class-based view for character detail."""

    model = Character
    template_name = "characters/character_details.html"


class CharacterListView(FilterView):
    """Class-based view for character list.

    This provides the following abilities:
    - Searching by `name` and `description`.
    - Filter by `age` and `universe`.
    - Page pagination.

    """

    model = Character
    paginate_by = 20
    queryset = Character.objects.order_by(
        "name",
    )
    filterset_class = CharacterFilter
    template_name = "characters/character_list.html"


class CharactersAutocompleteView(autocomplete.Select2QuerySetView):
    """Class-based view to auto-complete the `characters` field in filter."""

    def get_queryset(self) -> QuerySet:
        """Filter queryset by query parameters if it exists."""
        characters = Character.objects.order_by("name")
        if not self.q:
            return characters

        return characters.filter(name__icontains=self.q)


class UserCharacterListView(LoginRequiredMixin, CharacterListView):
    """Class-based view to display user's characters."""

    filterset_class = UserCharacterFilter
    template_name = "characters/user_character_list.html"

    def get_queryset(self) -> QuerySet:
        """Filter queryset by user to display only self characters."""
        return super().get_queryset().filter(
            user=self.request.user,
        ).select_related(
            "universe",
        )


class CharacterUpdateView(LoginRequiredMixin, generic.UpdateView):
    """Class-based view to edit the character details."""

    model = Character
    form_class = CharacterForm
    template_name = "characters/update_character.html"

    def get_queryset(self) -> QuerySet:
        """Filter queryset by user to allow edit only self characters."""
        return super().get_queryset().filter(
            user=self.request.user,
        ).select_related(
            "universe",
        )

    def get_success_url(self) -> str:
        """Redirect to details page after modification."""
        return reverse_lazy(
            "character-details",
            kwargs={
                "pk": self.object.id,
            },
        )


class CharacterCreateView(LoginRequiredMixin, generic.CreateView):
    """Class-based view to create new character."""

    model = Character
    form_class = CharacterForm
    template_name = "characters/create_character.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Set the current user to the form."""
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self) -> str:
        """Redirect to details page after creation."""
        return reverse_lazy(
            "character-details",
            kwargs={
                "pk": self.object.id,
            },
        )


class CharacterDeleteView(LoginRequiredMixin, generic.DeleteView):
    """Class-based view to delete character."""

    model = Character
    template_name = "characters/delete_character_confirm.html"
    success_url = reverse_lazy("user-character-list")

    def get_queryset(self) -> QuerySet:
        """Filter queryset by user to allow delete only self characters."""
        return super().get_queryset().filter(
            user=self.request.user,
        )
