from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class Genre(BaseModel):
    """Genre model for fanfiction creation."""

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=30,
        unique=True,
    )

    class Meta:
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")

    def __str__(self) -> str:
        return self.name
