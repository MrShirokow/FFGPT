from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel

from ..querysets import FanfictionQuerySet


class FanFiction(BaseModel):
    """Fanfiction model.

    Fanfiction is the main entity of the application. Each fanfiction belongs
    to one user, who can write the text for the fanfiction himself or generate
    it using the ChatGPT neural network.
    Fanfiction can be published or unpublished:
    - unpublished fanfictions are visible only to their authors.
    - published fanfictions are visible to all users.

    """

    title = models.CharField(
        verbose_name=_("Title"),
        max_length=50,
    )
    text = models.TextField(
        verbose_name=_("Text"),
    )
    is_published = models.BooleanField(
        verbose_name=_("Publication status"),
        default=False,
        help_text=_("Designates whether the fanfiction is published or not."),
    )
    publication_date = models.DateTimeField(
        verbose_name=_("Publication date"),
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        to="users.User",
        on_delete=models.CASCADE,
        related_name="fanfictions",
        verbose_name=_("User"),
    )
    genre = models.ForeignKey(
        to="fanfictions.Genre",
        on_delete=models.CASCADE,
        related_name="fanfictions",
        verbose_name=_("Genre"),
    )
    characters = models.ManyToManyField(
        to="characters.Character",
        related_name="fanfictions",
        verbose_name=_("Characters"),
    )

    objects = FanfictionQuerySet.as_manager()

    class Meta:
        verbose_name = _("Fanfiction")
        verbose_name_plural = _("Fanfictions")

    def __str__(self) -> str:
        return self.title

    def save(self, **kwargs):
        """Set `publication_date` if fanfiction is published."""
        if not self.publication_date and self.is_published:
            self.publication_date = timezone.now()
        elif not self.is_published and self.publication_date:
            self.publication_date = None
        return super().save(**kwargs)
