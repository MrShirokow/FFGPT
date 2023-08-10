from django.contrib import admin
from django.views.generic.base import RedirectView

from django.urls import include, path, reverse_lazy

from apps.core.views import IndexView

from .api_versions import urlpatterns as api_urlpatterns
from .debug import urlpatterns as debug_urlpatterns

urlpatterns = [
    path(
        "",
        RedirectView.as_view(url=reverse_lazy("fanfiction-list")),
        name="home",
    ),
    path("index/", IndexView.as_view(), name="index"),
    path("mission-control-center/", admin.site.urls),
    # Django Health Check url
    # See more details: https://pypi.org/project/django-health-check/
    # Custom checks at lib/health_checks
    path("health/", include("health_check.urls")),
    path("accounts/", include("apps.users.auth.urls")),
    path("user/", include("apps.users.urls")),
    path("characters/", include("apps.characters.urls")),
    path("fanfictions/", include("apps.fanfictions.urls")),
]

urlpatterns += api_urlpatterns
urlpatterns += debug_urlpatterns
