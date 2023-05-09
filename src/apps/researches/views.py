from dal import autocomplete

# from django.contrib.auth import get_permission_codename
from django.db.models import Q
from django.http import HttpRequest

from .models import Research


class ResearchAutocomplete(autocomplete.Select2QuerySetView):
    request: HttpRequest

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Research.objects.none()
        # codename = get_permission_codename("view", Research._meta)
        # if not self.request.user.has_perm("%s.%s" % (Research._meta, codename)):
        #     return Research.objects.none()

        return Research.objects.filter(Q(name__icontains=self.q) | Q(project__name__icontains=self.q))
