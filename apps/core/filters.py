from django.db.models import F, OrderBy
from django.utils.translation import gettext_lazy as _

from admin_auto_filters.filters import AutocompleteFilter

from libs.open_api.filters import OrderingFilterBackend


class UserEmailFilter(AutocompleteFilter):
    """Custom filter for searching by user email."""

    title = _("User")
    field_name = "user"


class GenreFilter(AutocompleteFilter):
    """Custom filter for searching by genre."""

    title = _("Genre")
    field_name = "genre"


class UniverseFilter(AutocompleteFilter):
    """Custom filter for searching by universe."""

    title = _("Universe")
    field_name = "universe"


class NullsLastOrderingFilterBackend(OrderingFilterBackend):
    """Ordering filter for moving null values to the end of queryset."""

    def filter_queryset(self, request, queryset, view):
        """Return filtered queryset with null values at the end."""
        ordering = self.get_ordering(request, queryset, view)

        if not ordering:
            return queryset

        ordering_fields = [
            OrderBy(
                F(field.lstrip("-")),
                descending=field.startswith("-"),
                nulls_last=True,
            ) for field in ordering
        ]
        return queryset.order_by(*ordering_fields)
