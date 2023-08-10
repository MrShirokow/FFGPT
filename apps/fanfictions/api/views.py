from django.db.models import F
from django.http import HttpRequest

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema

from apps.fanfictions.tasks import create_fanfiction_with_chatgpt, publish

from ...core.api.views import CRUDViewSet
from ..models import FanFiction
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    FanfictionChatGPTSerializer,
    FanfictionDelayedPublicationSerializer,
    FanFictionSerializer,
)


class FanfictionViewSet(CRUDViewSet):
    """ViewSet for viewing fanfictions."""

    queryset = FanFiction.objects.select_related(
        "user",
        "genre",
    ).prefetch_related(
        "characters",
    )
    serializer_class = FanFictionSerializer
    serializers_map = {
        "start_creation_task_with_chatgpt": FanfictionChatGPTSerializer,
        "delayed_publication": FanfictionDelayedPublicationSerializer,
    }
    permissions_map = {
        "list": (
            AllowAny,
        ),
        "update": (
            IsOwnerOrReadOnly,
        ),
        "destroy": (
            IsOwnerOrReadOnly,
        ),
        "delayed_publication": (
            IsOwnerOrReadOnly,
        ),
    }
    search_fields = (
        "title",
        "text",
        "characters__name",
    )
    ordering_fields = (
        "publication_date",
        "created",
        "modified",
    )
    filterset_fields = (
        "characters",
        "genre",
    )

    def get_queryset(self):
        """Return required queryset depending on the action."""
        if self.action == "list":
            return super().get_queryset().published().order_by(
                "-publication_date",
            )
        return super().get_queryset().available_for_user(
            user=self.request.user,
        )

    @extend_schema(responses=serializer_class(many=True))
    @action(
        detail=False,
        methods=["get"],
        url_name="user-list",
        url_path="user-list",
    )
    def user_list(self, request: HttpRequest, *args, **kwargs) -> Response:
        """Return list of fanfiction for request user."""
        queryset = self.filter_queryset(
            self.get_queryset().own(
                user_id=request.user.id,
            ).order_by(
                F("created").desc(nulls_last=True),
            ),
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(responses={200: None})
    @action(
        detail=False,
        methods=["post"],
        url_name="create-with-chatgpt",
        url_path="create-with-chatgpt",
    )
    def start_creation_task_with_chatgpt(
        self,
        request: HttpRequest,
        *args,
        **kwargs,
    ) -> Response:
        """Start task with request to ChatGPT and create new fanfiction."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        character_ids = [
            character.id for character in validated_data["characters"]
        ]

        create_fanfiction_with_chatgpt.delay(
            title=validated_data["title"],
            genre_id=validated_data["genre"].id,
            user_id=request.user.id,
            character_ids=character_ids,
        )
        return Response(status=status.HTTP_200_OK)

    @extend_schema(responses={200: None})
    @action(
        detail=True,
        methods=["post"],
        url_name="delayed-publication",
        url_path="delayed-publication",
    )
    def delayed_publication(
        self,
        request: HttpRequest,
        *args,
        **kwargs,
    ) -> Response:
        """Create task to publish fanfiction on the publication date."""
        fanfiction: FanFiction = self.get_object()
        if fanfiction.is_published:
            return Response(
                f"Fanfiction '{fanfiction.title}' has already been published.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        publish.apply_async(
            (
                fanfiction.id,
            ),
            eta=validated_data["publication_date"],
        )
        return Response(status=status.HTTP_200_OK)
