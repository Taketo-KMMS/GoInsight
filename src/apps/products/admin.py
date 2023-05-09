from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .forms import ProductForm
from .models import Product, ProductCategory, ProductMaker


@admin.register(ProductCategory)
class ProductCategoryAdmin(MPTTModelAdmin):
    mptt_level_indent = 12


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = ("code", "name", "created_at")


admin.site.register(ProductMaker)
