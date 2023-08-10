from django import forms
from django.utils.translation import gettext_lazy as _

from dal import autocomplete

from .models import FanFiction


class FanfictionCreateForm(forms.ModelForm):
    """Form with overridden `characters` field for creating new fanfiction."""

    class Meta:
        model = FanFiction
        fields = (
            "title",
            "genre",
            "text",
            "characters",
        )
        widgets = {
            "characters": autocomplete.ModelSelect2Multiple(
                url="characters-autocomplete",
            ),
            "genre": autocomplete.ModelSelect2(
                url="genres-autocomplete-create",
            ),
        }


class FanfictionUpdateForm(FanfictionCreateForm):
    """Form for updating fanfictions with additional field `is_published`."""

    class Meta(FanfictionCreateForm.Meta):
        fields = FanfictionCreateForm.Meta.fields + (
            "is_published",
        )
        widgets = {
            "characters": autocomplete.ModelSelect2Multiple(
                url="characters-autocomplete",
            ),
            "is_published": forms.RadioSelect(
                attrs={
                    "class": "form-check-input",
                },
                choices=(
                    (True, _("Published")),
                    (False, _("Unpublished")),
                ),
            ),
            "genre": autocomplete.ModelSelect2(
                url="genres-autocomplete-create",
            ),
        }


class FanfictionChatGPTCreateForm(FanfictionCreateForm):
    """Form for creating new fanfiction with ChatGPT."""

    class Meta(FanfictionCreateForm.Meta):
        fields = (
            "title",
            "genre",
            "characters",
        )


class FanfictionPublicationForm(forms.ModelForm):
    """Form for delayed publication of fanfictions."""

    publication_date = forms.DateField(
        widget=forms.widgets.DateInput(
            attrs={
                "type": "date",
                "class": "form-control",
            },
        ),
    )
    publication_time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={
                "type": "time",
                "class": "form-control",
            },
        ),
    )

    class Meta:
        model = FanFiction
        fields = ("id",)
