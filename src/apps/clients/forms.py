from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from apps.researches.models import Project

from .models import ClientGroup

projects_label = ClientGroup._meta.get_field("projects").verbose_name


class ClientGroupForm(forms.ModelForm):
    projects = forms.ModelMultipleChoiceField(
        Project.objects.all(),
        label=projects_label,
        blank=False,
        widget=FilteredSelectMultiple(projects_label, is_stacked=False),
    )

    class Meta:
        model = ClientGroup
        fields = "__all__"
