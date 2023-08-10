import factory

from apps.users.factories import UserFactory

from ..models import FanFiction
from .genre import GenreFactory


class FanFictionFactory(factory.django.DjangoModelFactory):
    """Factory to generate FanFiction test instance."""

    title = factory.Faker("sentence", nb_words=3)
    text = factory.Faker("sentence", nb_words=100)
    is_published = factory.Faker("boolean")
    user = factory.SubFactory(UserFactory)
    genre = factory.SubFactory(GenreFactory)

    class Meta:
        model = FanFiction

    @factory.post_generation
    def characters(self, create, extracted, **kwargs) -> None:
        """Fill `characters` field."""
        if not create:
            return

        if extracted:
            # pylint: disable=no-member
            self.characters.set(extracted)
