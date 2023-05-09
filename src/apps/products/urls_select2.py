from django.urls import path

from .views import ProductAutocomplete

app_name = "products_select2"

urlpatterns = [path("", ProductAutocomplete.as_view(), name="index")]
