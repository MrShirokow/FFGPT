from django.db.models import QuerySet
from django.http import HttpRequest

from dal import autocomplete

from ..models import Universe


class UniverseAutocompleteView(autocomplete.Select2QuerySetView):
    """Class-based view to auto-complete the `universe` field."""

    def get_queryset(self) -> QuerySet:
        """Filter queryset by query parameters if it exists."""
        universes = Universe.objects.order_by("name")
        if not self.q:
            return universes

        return universes.filter(name__icontains=self.q)

    def has_add_permission(self, request: HttpRequest):
        """Return True if the user has the permission to add a model.

        It's overridden because all authenticated users can create `Universe`
        model objects.

        """
        return request.user.is_authenticated
