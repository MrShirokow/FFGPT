import factory

from ..models import Universe


class UniverseFactory(factory.django.DjangoModelFactory):
    """Factory to generate Universe test instance."""

    name = factory.Iterator(("Marvel", "Real", "Magic"))

    class Meta:
        model = Universe
        django_get_or_create = (
            "name",
        )
