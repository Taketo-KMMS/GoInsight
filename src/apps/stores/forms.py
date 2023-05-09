from dal import autocomplete
from django import forms

from .models import Shelf, ShelfProductAlloc, StoreCategory


class ShelfForm(forms.ModelForm):
    store_category = forms.ModelChoiceField(
        queryset=StoreCategory.objects.select_related("store_branch", "store_branch__store"),
        label=Shelf._meta.get_field("store_category").verbose_name,
    )

    class Meta:
        model = Shelf
        fields = ("store_category", "start_date", "end_date", "file")


class ShelfProductAllocForm(forms.ModelForm):
    class Meta:
        model = ShelfProductAlloc
        fields = "__all__"
        widgets = {
            "product": autocomplete.ModelSelect2(
                url="products_select2:index",
                attrs={
                    "data-minimum-input-length": 2,
                },
            )
        }
