from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    UpdateView,
)

from django_filters.views import FilterView

from ..filters import FanfictionFilter, UserFanfictionFilter
from ..forms import (
    FanfictionChatGPTCreateForm,
    FanfictionCreateForm,
    FanfictionPublicationForm,
    FanfictionUpdateForm,
)
from ..models import FanFiction
from ..tasks import create_fanfiction_with_chatgpt, publish


class FanfictionDetailView(DetailView):
    """Class-based view for fanfiction detail."""

    model = FanFiction
    template_name = "fanfictions/fanfiction_details.html"

    def get_queryset(self) -> QuerySet:
        """Filter queryset by user.

        It's needed to prohibit view unpublished fanfictions of other users.

        """
        return super().get_queryset().available_for_user(
            user=self.request.user,
        ).select_related(
            "user",
            "genre",
        ).prefetch_related(
            "characters",
        )


class FanfictionListView(FilterView):
    """Class-based view for fanfiction list.

    This provides the following abilities:
    - Searching by `characters`, `title` and `text`.
    - Filter by `character` and `genre`.
    - Page pagination.

    """

    model = FanFiction
    paginate_by = 5
    queryset = FanFiction.objects.select_related(
        "genre",
    ).filter(
        is_published=True,
    ).order_by(
        "-publication_date",
    )
    filterset_class = FanfictionFilter
    template_name = "fanfictions/fanfiction_list.html"


class FanfictionUpdateView(LoginRequiredMixin, UpdateView):
    """Class-based view to edit the fanfiction details."""

    model = FanFiction
    form_class = FanfictionUpdateForm
    template_name = "fanfictions/update_fanfiction.html"

    def get_queryset(self) -> QuerySet:
        """Filter queryset by user to allow edit only self fanfictions."""
        return super().get_queryset().filter(
            user=self.request.user,
        ).select_related(
            "genre",
        )

    def get_success_url(self) -> str:
        """Redirect to details page after modification."""
        return reverse_lazy(
            "fanfiction-details",
            kwargs={
                "pk": self.object.id,
            },
        )


class FanfictionCreateView(LoginRequiredMixin, CreateView):
    """Class-based view to create new fanfiction."""

    model = FanFiction
    form_class = FanfictionCreateForm
    template_name = "fanfictions/create_fanfiction.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Set the current user to the form."""
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self) -> str:
        """Redirect to details page after creation."""
        return reverse_lazy(
            "fanfiction-details",
            kwargs={
                "pk": self.object.id,
            },
        )


class FanfictionDeleteView(LoginRequiredMixin, DeleteView):
    """Class-based view to delete fanfiction."""

    model = FanFiction
    template_name = "fanfictions/delete_fanfiction_confirm.html"
    success_url = reverse_lazy("fanfiction-list")

    def get_queryset(self) -> QuerySet:
        """Filter queryset by user to allow delete only self fanfictions."""
        return super().get_queryset().filter(
            user=self.request.user,
        )


class UserFanfictionListView(LoginRequiredMixin, FilterView):
    """Class-based view to display user's fanfictions."""

    model = FanFiction
    paginate_by = 5
    filterset_class = UserFanfictionFilter
    template_name = "fanfictions/user_fanfiction_list.html"

    def get_queryset(self) -> QuerySet:
        """Filter queryset by user to display only self fanfictions."""
        return super().get_queryset().filter(
            user=self.request.user,
        ).select_related(
            "genre",
        ).order_by(
            F("created").desc(nulls_last=True),
        )


class FanfictionChatGPTCreateView(LoginRequiredMixin, FormView):
    """Class-based view to create new fanfiction with ChatGPT."""

    form_class = FanfictionChatGPTCreateForm
    template_name = "fanfictions/create_fanfiction_with_chatgpt.html"
    success_url = reverse_lazy("chatgpt-success-page")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Start task with request to ChatGPT and create new fanfiction."""
        create_fanfiction_with_chatgpt.delay(
            title=form.cleaned_data["title"],
            genre_id=form.cleaned_data["genre"].id,
            user_id=self.request.user.id,
            character_ids=[
                character.id for character in form.cleaned_data["characters"]
            ],
        )
        return super().form_valid(form)


class FanfictionDelayedPublicationView(DetailView, FormView):
    """Class-based view for delayed publication of fanfictions."""

    model = FanFiction
    form_class = FanfictionPublicationForm
    template_name = "fanfictions/delayed_publication.html"
    success_url = reverse_lazy("delayed-publication-success")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Create task to publish fanfiction on the publication date."""
        publication_date = datetime.combine(
            date=form.cleaned_data["publication_date"],
            time=form.cleaned_data["publication_time"],
        )
        publish.apply_async(
            (
                self.get_object().id,
            ),
            eta=publication_date,
        )
        return super().form_valid(form)
