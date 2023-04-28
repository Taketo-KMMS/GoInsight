from django import forms
from nested_admin.formsets import NestedInlineFormSet

from .models import Shelf, ShelfArea, StoreCategory


class ShelfForm(forms.ModelForm):
    store_category = forms.ModelChoiceField(
        queryset=StoreCategory.objects.select_related("store_branch", "store_branch__store"),
        label=Shelf._meta.get_field("store_category").verbose_name,
    )

    class Meta:
        model = Shelf
        fields = ("store_category", "start_date", "end_date", "file")


class ShelfAreaFormSet(NestedInlineFormSet):
    model = ShelfArea
