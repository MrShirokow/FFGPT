import random

from faker import Faker

from apps.characters.factories import CharacterFactory, UniverseFactory
from apps.fanfictions.factories import FanFictionFactory
from apps.users.factories import UserFactory

USER_COUNT = 10
GENRE_COUNT = 3


def run() -> None:
    """Create model entries in the database."""
    faker = Faker()
    UniverseFactory.create_batch(GENRE_COUNT)

    for _ in range(USER_COUNT):
        user = UserFactory.create(email=faker.unique.email())
        CharacterFactory.create_batch(random.randint(2, 5), user=user)
        characters = user.characters.order_by("?")[:random.randint(2, 5)]
        FanFictionFactory.create_batch(
            random.randint(2, 5),
            user=user,
            characters=characters,
        )
