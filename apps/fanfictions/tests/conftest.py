from typing import Sequence

import pytest

from apps.characters.factories import CharacterFactory
from apps.characters.models import Character

from ..factories import FanFictionFactory
from ..models import FanFiction


@pytest.fixture
def characters() -> list[Character]:
    """Return prepared character data list."""
    return CharacterFactory.create_batch(5)


@pytest.fixture
def published_fanfiction(
    characters: Sequence[Character],
) -> FanFiction:
    """Return published fanfiction object."""
    return FanFictionFactory.create(
        is_published=True,
        characters=characters,
    )


@pytest.fixture
def unpublished_fanfiction(
    characters: Sequence[Character],
) -> FanFiction:
    """Return unpublished fanfiction object."""
    return FanFictionFactory.create(
        is_published=False,
        characters=characters,
    )


@pytest.fixture
def prepare_fanfictions(
    characters: Sequence[Character],
    published_fanfiction: FanFiction,
    unpublished_fanfiction: FanFiction,
):
    """Prepare additional fanfictions for tests."""
    FanFictionFactory.create_batch(
        size=3,
        characters=characters,
    )
