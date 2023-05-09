from django.urls import path

from .views import ResearchAutocomplete

app_name = "researches_select2"

urlpatterns = [path("", ResearchAutocomplete.as_view(), name="index")]
