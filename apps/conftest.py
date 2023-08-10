from rest_framework import test

import pytest

from apps.users.factories import AdminUserFactory, UserFactory
from apps.users.models import User


@pytest.fixture
def user(django_db_blocker) -> User:
    """Create user for testing."""
    with django_db_blocker.unblock():
        return UserFactory()


@pytest.fixture
def admin_user(django_db_blocker) -> User:
    """Create admin user for testing."""
    with django_db_blocker.unblock():
        return AdminUserFactory()


@pytest.fixture
def api_client() -> test.APIClient:
    """Create api client."""
    return test.APIClient()


@pytest.fixture
def user_api_client(
    user: User,
    api_client: test.APIClient,
) -> test.APIClient:
    """Return api client with authorized user."""
    api_client.force_authenticate(user=user)
    return api_client
