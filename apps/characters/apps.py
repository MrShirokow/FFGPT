from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CharactersConfig(AppConfig):
    """Default configuration for Characters app."""

    name = "apps.characters"
    verbose_name = _("Characters")
