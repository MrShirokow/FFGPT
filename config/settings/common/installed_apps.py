from .health_check import HEALTH_CHECKS_APPS

# Application definition
INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
)

DRF_PACKAGES = (
    "rest_framework",
    "django_filters",
    "knox",
    "drf_spectacular",
    "drf_standardized_errors",
)

THIRD_PARTY = (
    "storages",
    "imagekit",
    "django_celery_beat",
    "django_extensions",
    "admin_auto_filters",
    "dal",
    "dal_select2",
)

LOCAL_APPS = (
    "apps.core",
    "apps.users",
    "apps.fanfictions",
    "apps.characters",
)

INSTALLED_APPS += DRF_PACKAGES + THIRD_PARTY + HEALTH_CHECKS_APPS + LOCAL_APPS
