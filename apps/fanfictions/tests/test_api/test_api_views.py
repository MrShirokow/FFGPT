from functools import partial
from typing import Any, Sequence

from django.urls import reverse

from rest_framework import status, test
from rest_framework.response import Response

import pytest

from apps.characters.models import Character
from apps.fanfictions.factories import GenreFactory

from ...api.serializers import FanFictionSerializer
from ...factories import FanFictionFactory
from ...models import FanFiction, Genre


def get_fanfiction_url(action_name: str, args=None):
    """Get URL for fanfiction view action."""
    return reverse(f"v1:fanfiction-{action_name}", args=args)


get_fanfiction_list_url = partial(get_fanfiction_url, action_name="list")
get_fanfiction_detail_url = partial(get_fanfiction_url, action_name="detail")


@pytest.fixture
def genre() -> Genre:
    """Create `Genre` object for testing."""
    return GenreFactory()


@pytest.fixture
def fanfiction_create_update_data(
    genre: Genre,
    characters: Sequence[Character],
) -> dict[str, Any]:
    """Return data to create/update fanfiction."""
    fanfiction = FanFictionFactory.build(
        genre=genre,
        characters=characters,
    )
    return FanFictionSerializer(instance=fanfiction).data


@pytest.mark.usefixtures("prepare_fanfictions")
def test_get_fanfiction_list(user_api_client: test.APIClient):
    """Test the fanfiction list consists only of published fanfictions."""
    response: Response = user_api_client.get(get_fanfiction_list_url())
    assert response.status_code == status.HTTP_200_OK, response.data
    assert all(
        fanfiction_dto["is_published"]
        for fanfiction_dto in response.data["results"]
    )


def test_user_cannot_view_other_users_unpublished_fanfictions(
    user_api_client: test.APIClient,
    unpublished_fanfiction: FanFiction,
):
    """Test user cannot view unpublished fanfictions of other users."""
    response: Response = user_api_client.get(
        path=get_fanfiction_detail_url(args=[unpublished_fanfiction.id]),
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.data


@pytest.mark.parametrize(
    ["fanfiction", "response_status_code"],
    [
        [
            pytest.lazy_fixtures("published_fanfiction"),
            status.HTTP_403_FORBIDDEN,
        ],
        [
            pytest.lazy_fixtures("unpublished_fanfiction"),
            status.HTTP_404_NOT_FOUND,
        ],
    ],
)
def test_user_cannot_delete_other_users_fanfictions(
    user_api_client: test.APIClient,
    fanfiction: FanFiction,
    response_status_code: int,
):
    """Test user cannot delete fanfictions of other users."""
    response: Response = user_api_client.delete(
        path=get_fanfiction_detail_url(args=[fanfiction.id]),
    )
    assert response.status_code == response_status_code, response.data


@pytest.mark.parametrize(
    ["fanfiction", "response_status_code"],
    [
        [
            pytest.lazy_fixtures("published_fanfiction"),
            status.HTTP_403_FORBIDDEN,
        ],
        [
            pytest.lazy_fixtures("unpublished_fanfiction"),
            status.HTTP_404_NOT_FOUND,
        ],
    ],
)
def test_user_cannot_update_other_users_fanfictions(
    user_api_client: test.APIClient,
    fanfiction: FanFiction,
    fanfiction_create_update_data: dict[str, Any],
    response_status_code: int,
):
    """Test user cannot update fanfictions of other users."""
    response: Response = user_api_client.put(
        path=get_fanfiction_detail_url(args=[fanfiction.id]),
        data=fanfiction_create_update_data,
    )
    assert response.status_code == response_status_code, response.data


def test_unauthorized_user_cannot_create_fanfiction(
    api_client: test.APIClient,
    fanfiction_create_update_data: dict[str, Any],
):
    """Test unauthorized user cannot create new fanfiction."""
    response: Response = api_client.post(
        path=get_fanfiction_list_url(),
        data=fanfiction_create_update_data,
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.data
