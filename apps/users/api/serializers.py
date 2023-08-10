from django.contrib.auth import get_user_model

from apps.core.api.serializers import ModelBaseSerializer


class UserSerializer(ModelBaseSerializer):
    """Serializer for representing `User`."""

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "avatar",
            "last_login",
            "created",
            "modified",
        )
        read_only_fields = (
            "email",
            "last_login",
            "created",
            "modified",
        )
