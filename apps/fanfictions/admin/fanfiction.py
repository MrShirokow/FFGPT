from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.core.admin import BaseAdmin
from apps.core.filters import GenreFilter, UserEmailFilter

from ..models import FanFiction


@admin.register(FanFiction)
class FanFictionAdmin(BaseAdmin):
    """UI for FanFiction model."""

    ordering = (
        "id",
    )
    list_display = (
        "id",
        "title",
        "is_published",
        "publication_date",
        "_get_user_email",
        "_get_genre_name",
    )
    list_display_links = (
        "id",
        "title",
    )
    list_filter = (
        GenreFilter,
        UserEmailFilter,
        "is_published",
    )
    fieldsets = (
        (
            None, {
                "fields": (
                    "title",
                    "text",
                    "is_published",
                ),
            },
        ),
        (
            _("Relationship info"), {
                "fields": (
                    "user",
                    "genre",
                    "characters",
                ),
            },
        ),
    )
    autocomplete_fields = (
        "characters",
    )
    search_fields = (
        "title",
        "text",
    )

    @admin.display(description="User", ordering="user__email")
    def _get_user_email(self, fanfiction: FanFiction) -> str:
        return fanfiction.user.email

    @admin.display(description="Genre", ordering="genre__name")
    def _get_genre_name(self, fanfiction: FanFiction) -> str:
        return fanfiction.genre.name
