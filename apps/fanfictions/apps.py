from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FanFictionsConfig(AppConfig):
    """Default configuration for FanFictions app."""

    name = "apps.fanfictions"
    verbose_name = _("FanFictions")
