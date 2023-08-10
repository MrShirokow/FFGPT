# pylint: disable=duplicate-code
from django.contrib import admin

from apps.core.admin import BaseAdmin

from ..models import Genre


@admin.register(Genre)
class GenreAdmin(BaseAdmin):
    """UI for Genre model."""

    ordering = (
        "id",
    )
    list_display = (
        "id",
        "name",
    )
    list_display_links = list_display
    fieldsets = (
        (
            None, {
                "fields": (
                    "name",
                ),
            },
        ),
    )
    search_fields = (
        "name",
    )
