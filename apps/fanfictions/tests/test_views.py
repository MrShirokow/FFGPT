from http import HTTPStatus

from django.db.models import QuerySet
from django.test import Client
from django.urls import reverse

import pytest

from apps.users.factories import UserFactory

from ..models import FanFiction


@pytest.fixture
def authorized_client(client: Client) -> Client:
    """Return authorized client for tests."""
    user = UserFactory()
    client.force_login(user)
    return client


@pytest.mark.usefixtures("prepare_fanfictions")
def test_only_published_fanfictions_are_visible_in_list(client: Client):
    """Test display of only published fanfictions on fanfiction list page."""
    response = client.get(reverse("fanfiction-list"))
    fanfiction_list: QuerySet = response.context["fanfiction_list"]
    assert all(fanfiction.is_published for fanfiction in fanfiction_list)


def test_user_cannot_view_other_users_unpublished_fanfictions(
    authorized_client: Client,
    unpublished_fanfiction: FanFiction,
):
    """Test restrictions on access to unpublished fanfiction of other users."""
    response = authorized_client.get(
        reverse(
            "fanfiction-details",
            args=[unpublished_fanfiction.id],
        ),
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize(
    "request_url",
    [
        "update-fanfiction",
        "delete-fanfiction",
    ],
)
def test_access_to_modify_only_self_fanfictions(
    request_url: str,
    authorized_client: Client,
    published_fanfiction: FanFiction,
):
    """Test user's ability to update/delete only him fanfiction."""
    response = authorized_client.get(
        reverse(
            request_url,
            args=[published_fanfiction.id],
        ),
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
