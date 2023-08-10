from django.contrib.auth import get_user_model

from rest_framework.permissions import IsAdminUser

from ...core.api.views import ReadOnlyViewSet
from . import serializers

User = get_user_model()


class UsersViewSet(ReadOnlyViewSet):
    """ViewSet for viewing accounts."""

    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (IsAdminUser,)
    search_fields = (
        "first_name",
        "last_name",
    )
    ordering_fields = (
        "first_name",
        "last_name",
    )
