from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"", views.FanfictionViewSet, basename="fanfiction")
urlpatterns = router.urls
