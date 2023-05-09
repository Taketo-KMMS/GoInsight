# from dal import autocomplete
# from django import forms

# from apps.products.models import Product
# from apps.researches.models import Research


# class EventSearchForm(forms.Form):
#     research = forms.ModelChoiceField(
#         Research.objects.all(),
#         required=False,
#         widget=autocomplete.ModelSelect2(
#             url="researches_select2:index",
#             attrs={
#                 "data-minimum-input-length": 2,
#             },
#         ),
#     )


# class ProductEventSearchForm(EventSearchForm):
#     product = forms.ModelChoiceField(
#         Product.objects.all(),
#         required=False,
#         widget=autocomplete.ModelSelect2(
#             url="products_select2:index",
#             attrs={
#                 "data-minimum-input-length": 2,
#             },
#         ),
#     )
