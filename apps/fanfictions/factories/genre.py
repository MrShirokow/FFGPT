import factory

from ..models import Genre


class GenreFactory(factory.django.DjangoModelFactory):
    """Factory to generate Genre test instance."""

    name = factory.Iterator(("Thriller", "Drama", "Comedy"))

    class Meta:
        model = Genre
        django_get_or_create = (
            "name",
        )
