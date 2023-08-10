# pylint: disable=duplicate-code
from django.contrib import admin

from apps.core.admin import BaseAdmin

from ..models import Universe


@admin.register(Universe)
class UniverseAdmin(BaseAdmin):
    """UI for Universe model."""

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
