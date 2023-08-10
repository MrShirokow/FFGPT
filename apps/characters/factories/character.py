import factory
from factory.fuzzy import FuzzyChoice, FuzzyInteger

from apps.users.factories import UserFactory

from ..models import Character
from .universe import UniverseFactory


class CharacterFactory(factory.django.DjangoModelFactory):
    """Factory to generate Character test instance."""

    name = factory.Faker("name")
    age = FuzzyInteger(5, 30)
    gender = FuzzyChoice(Character.GenderChoice.values)
    description = factory.Faker("text")
    user = factory.SubFactory(UserFactory)
    universe = factory.SubFactory(UniverseFactory)

    class Meta:
        model = Character
