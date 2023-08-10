from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.CharacterListView.as_view(),
        name="characters",
    ),
    path(
        "<int:pk>/",
        views.CharacterDetailView.as_view(),
        name="character-details",
    ),
    path(
        "autocomplete/",
        views.CharactersAutocompleteView.as_view(),
        name="characters-autocomplete",
    ),
    path(
        "create/",
        views.CharacterCreateView.as_view(),
        name="create-character",
    ),
    path(
        "<int:pk>/update/",
        views.CharacterUpdateView.as_view(),
        name="update-character",
    ),
    path(
        "<int:pk>/delete/",
        views.CharacterDeleteView.as_view(),
        name="delete-character",
    ),
    path(
        "universes/autocomplete/",
        views.UniverseAutocompleteView.as_view(),
        name="universes-autocomplete",
    ),
    path(
        "universes/autocomplete-create/",
        views.UniverseAutocompleteView.as_view(
            create_field="name",
        ),
        name="universes-autocomplete-create",
    ),
]
