from rest_framework import serializers

from apps.core.api.serializers import BaseSerializer, ModelBaseSerializer
from apps.users.api.serializers import UserSerializer

from ..models import FanFiction


class FanfictionChatGPTSerializer(ModelBaseSerializer):
    """Serializer for representing `Fanfiction` creation data for ChatGPT."""

    user = UserSerializer(
        default=serializers.CurrentUserDefault(),
        read_only=True,
    )

    class Meta:
        model = FanFiction
        fields = (
            "id",
            "title",
            "is_published",
            "publication_date",
            "user",
            "genre",
            "characters",
            "created",
            "modified",
        )
        read_only_fields = (
            "publication_date",
            "created",
            "modified",
        )

    def create(self, validated_data: dict):
        """Override to add `user` field."""
        validated_data.update(
            user=self._user,
        )
        return super().create(validated_data)


class FanFictionSerializer(FanfictionChatGPTSerializer):
    """Serializer for representing `Fanfiction`."""

    class Meta(FanfictionChatGPTSerializer.Meta):
        fields = FanfictionChatGPTSerializer.Meta.fields + ("text",)


# pylint: disable=abstract-method
class FanfictionDelayedPublicationSerializer(BaseSerializer):
    """Serializer for representing date and time for delayed publication."""

    publication_date = serializers.DateTimeField()

    class Meta:
        fields = (
            "publication_date",
        )
