import re

from dal import autocomplete
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpRequest

from .models import Product


class ProductAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    request: HttpRequest

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Product.objects.none()

        inputs = [i for i in re.split(r"\s+", self.q) if i]
        if len(inputs) == 0:
            return Product.objects.none()

        cond = Q()
        for i in inputs:
            cond |= Q(name__icontains=i)
        if len(inputs) == 1 and len(inputs[0]) > 8:
            cond |= Q(code=self.q)

        return Product.objects.filter(cond)
