from typing import Sequence

import pytest
from faker import Faker

from apps.characters.models import Character

from ..factories import FanFictionFactory
from ..filters import FanfictionFilter, UserFanfictionFilter
from ..models import FanFiction


def test_fanfiction_filter(characters: Sequence[Character], faker: Faker):
    """Test correctness of queryset after filter by `FanfictionFilter`."""
    search_text = "test text"
    not_matched_text = "bad"  # Text that doesn't exactly contain `search_text`

    FanFictionFactory.create(
        title=not_matched_text,
        text=not_matched_text * 10,
        characters=characters,
    )
    fanfiction = FanFictionFactory.create(
        title=search_text,
        text=faker.text() + search_text,
        characters=characters,
    )
    filter_data = {
        "search": search_text,
        "genre": fanfiction.genre_id,
        "characters": fanfiction.characters.first().id,
    }

    filtered_fanfictions = FanfictionFilter(
        data=filter_data,
        queryset=FanFiction.objects.all(),
    ).qs
    assert filtered_fanfictions.count() == 1


@pytest.mark.parametrize(
    "is_published",
    [
        True,
        False,
    ],
)
@pytest.mark.usefixtures("prepare_fanfictions")
def test_user_fanfiction_filter(is_published: bool):
    """Test correctness of queryset after filter by `UserFanfictionFilter`."""
    filtered_fanfictions = UserFanfictionFilter(
        data={
            "is_published": is_published,
        },
        queryset=FanFiction.objects.all(),
    ).qs

    assert all(
        fanfiction.is_published is is_published
        for fanfiction in filtered_fanfictions
    )
