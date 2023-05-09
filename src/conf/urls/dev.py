from django.urls import include, path

from .base import urlpatterns

urlpatterns = [path("__debug__/", include("debug_toolbar.urls")), *urlpatterns]
