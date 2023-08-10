from django.urls import path

from apps.characters.views import UserCharacterListView
from apps.fanfictions.views import UserFanfictionListView

from .views import UserPasswordChangeView, UserProfileView

urlpatterns = [
    path(
        "profile/",
        UserProfileView.as_view(),
        name="profile",
    ),
    path(
        "password/",
        UserPasswordChangeView.as_view(),
        name="change-password",
    ),
    path(
        "fanfictions/",
        UserFanfictionListView.as_view(),
        name="user-fanfiction-list",
    ),
    path(
        "characters/",
        UserCharacterListView.as_view(),
        name="user-character-list",
    ),
]
