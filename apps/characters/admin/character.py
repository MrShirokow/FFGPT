from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.core.admin import BaseAdmin
from apps.core.filters import UniverseFilter, UserEmailFilter

from ..models import Character


@admin.register(Character)
class CharacterAdmin(BaseAdmin):
    """UI for Character model."""

    ordering = (
        "id",
    )
    list_display = (
        "id",
        "name",
        "age",
        "gender",
        "_get_user_email",
        "_get_universe_name",
    )
    list_display_links = (
        "id",
        "name",
    )
    list_filter = (
        "gender",
        UserEmailFilter,
        UniverseFilter,
    )
    fieldsets = (
        (
            None, {
                "fields": (
                    "name",
                    "age",
                    "gender",
                    "description",
                ),
            },
        ),
        (
            _("Relationship info"), {
                "fields": (
                    "user",
                    "universe",
                ),
            },
        ),
    )
    search_fields = (
        "name",
    )

    @admin.display(description="User", ordering="user__email")
    def _get_user_email(self, character: Character) -> str:
        return character.user.email

    @admin.display(description="Universe", ordering="universe__name")
    def _get_universe_name(self, character: Character) -> str:
        return character.universe.name
