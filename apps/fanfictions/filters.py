from django import forms
from django.db.models import F, OrderBy, Q, QuerySet
from django.forms.widgets import TextInput
from django.utils.translation import gettext_lazy as _

import django_filters
from dal import autocomplete

from apps.characters.models import Character

from .models import FanFiction, Genre


class NullsLastOrderingFilter(django_filters.OrderingFilter):
    """Ordering filter for moving null values to the end of queryset."""

    def get_ordering_value(self, param):
        """Set null values to the end of queryset after ordering."""
        value = super().get_ordering_value(param)
        return OrderBy(
            F(value.lstrip("-")),
            descending=value.startswith("-"),
            nulls_last=True,
        )


class FanfictionFilter(django_filters.FilterSet):
    """Filter for `Fanfiction` model."""

    characters = django_filters.ModelMultipleChoiceFilter(
        queryset=Character.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(
            url="characters-autocomplete",
            attrs={"placeholder": _("Choose characters")},
        ),
        label=_("Choose characters"),
    )
    search = django_filters.CharFilter(
        method="search_filter",
        label=_("Search"),
        widget=TextInput(attrs={"placeholder": _("Search")}),
    )
    genre = django_filters.ModelChoiceFilter(
        queryset=Genre.objects.all(),
        widget=autocomplete.ModelSelect2(
            url="genres-autocomplete",
        ),
    )

    class Meta:
        model = FanFiction
        fields = "__all__"

    # pylint: disable=unused-argument
    def search_filter(self, queryset: QuerySet, name, value) -> QuerySet:
        """Filter by `text` and `title` fields with `icontains` lookup."""
        return queryset.filter(
            Q(title__icontains=value)
            | Q(text__icontains=value),
        )


class UserFanfictionFilter(FanfictionFilter):
    """Filter for `Fanfiction` model at user fanfiction list page."""

    _is_published_choices = (
        (True, _("Published")),
        (False, _("Unpublished")),
        (None, _("All")),
    )
    is_published = django_filters.BooleanFilter(
        field_name="is_published",
        widget=forms.RadioSelect(
            attrs={
                "class": "form-check-input",
            },
            choices=_is_published_choices,
        ),
        label=_("Choose publication status"),
    )
    order_by = NullsLastOrderingFilter(
        fields=(
            ("created", _("created")),
            ("modified", _("modified")),
            ("publication_date", _("publication")),
        ),
    )
