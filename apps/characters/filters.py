from django.db.models import Q, QuerySet
from django.forms.widgets import TextInput
from django.utils.translation import gettext_lazy as _

import django_filters
from dal import autocomplete

from apps.fanfictions.filters import NullsLastOrderingFilter

from .models import Character, Universe


class CharacterFilter(django_filters.FilterSet):
    """Filter for `Character` model."""

    search = django_filters.CharFilter(
        method="search_filter",
        label=_("Search"),
        widget=TextInput(attrs={"placeholder": _("Search")}),
    )
    age = django_filters.NumberFilter(lookup_expr="exact")
    universe = django_filters.ModelChoiceFilter(
        queryset=Universe.objects.all(),
        label=_("Universe"),
        empty_label="Select a universe",
        widget=autocomplete.ModelSelect2(
            url="universes-autocomplete",
        ),
    )

    class Meta:
        model = Character
        fields = {
            "name": ["iexact"],
            "description": ["iexact"],
            "age": ["exact"],
        }

    # pylint: disable=unused-argument
    def search_filter(self, queryset: QuerySet, name, value) -> QuerySet:
        """Filter by `name`, `description` fields."""
        return queryset.filter(
            Q(name__icontains=value)
            | Q(description__icontains=value),
        )


class UserCharacterFilter(CharacterFilter):
    """Filter for `Character` model at user character list page."""

    order_by = NullsLastOrderingFilter(
        fields=(
            ("created", _("created")),
            ("modified", _("modified")),
        ),
    )
