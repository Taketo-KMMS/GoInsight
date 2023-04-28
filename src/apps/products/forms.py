from django import forms
from mptt.forms import TreeNodeChoiceField

from common.utils import normalize_string

from .models import Product, ProductCategory


class ProductForm(forms.ModelForm):
    category = TreeNodeChoiceField(
        ProductCategory.objects.all(), required=False, label=Product._meta.get_field("category").verbose_name
    )

    class Meta:
        model = Product
        fields = ("code", "name", "maker", "category")

    def clean_name(self):
        name = self.ceaned_data["name"]
        if name := self.ceaned_data["name"]:
            return normalize_string(name)
