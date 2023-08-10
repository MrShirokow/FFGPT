# pylint: disable=duplicate-code
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class Universe(BaseModel):
    """Universe model for characters."""

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=30,
        unique=True,
    )

    class Meta:
        verbose_name = _("Universe")
        verbose_name_plural = _("Universes")

    def __str__(self) -> str:
        return self.name
