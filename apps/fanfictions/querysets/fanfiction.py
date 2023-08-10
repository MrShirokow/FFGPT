from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
from django.db import models


class FanfictionQuerySet(models.QuerySet):
    """Custom queryset with additional methods."""

    def published(self):
        """Return list of published fanfictions."""
        return self.filter(is_published=True)

    def available_for_user(self, user: AbstractBaseUser | AnonymousUser):
        """Return available to view derails list of fanfictions for user."""
        filter_options = models.Q(is_published=True)
        if user.is_authenticated:
            filter_options |= models.Q(user=user, is_published=False)
        return self.filter(filter_options)

    def own(self, user_id: int):
        """Return list of user fanfictions."""
        return self.filter(user_id=user_id)
