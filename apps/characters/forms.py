from django import forms

from dal import autocomplete

from .models import Character


class CharacterForm(forms.ModelForm):
    """Form with overridden widget for `universe` field."""

    class Meta:
        model = Character
        fields = (
            "name",
            "universe",
            "gender",
            "age",
            "description",
        )
        widgets = {
            "universe": autocomplete.ModelSelect2(
                url="universes-autocomplete-create",
            ),
        }
