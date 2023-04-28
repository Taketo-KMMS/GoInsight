from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from nested_admin import nested

from .forms import ShelfAreaFormSet, ShelfForm
from .models import (
    Shelf,
    ShelfArea,
    ShelfAreaRect,
    ShelfProductAlloc,
    ShelfProductAllocRect,
    Store,
    StoreBranch,
    StoreCategory,
)


class StoreCategoryInline(nested.NestedStackedInline):
    model = StoreCategory

    def get_queryset(self, request: HttpRequest):
        qs: "QuerySet[StoreCategory]" = super().get_queryset(request)
        return qs.select_related("store_branch", "store_branch__store")


class StoreBranchInline(nested.NestedStackedInline):
    extra = 1
    model = StoreBranch
    inlines = [StoreCategoryInline]

    def get_queryset(self, request: HttpRequest):
        qs: "QuerySet[StoreBranch]" = super().get_queryset(request)
        return qs.select_related("store")


@admin.register(Store)
class StoreAdmin(nested.NestedModelAdmin):
    inlines = [StoreBranchInline]


class ShelfAreaRectInline(nested.NestedTabularInline):
    model = ShelfAreaRect


class ShelfAreaInline(nested.NestedStackedInline):
    extra = 1
    model = ShelfArea
    inlines = [ShelfAreaRectInline]
    formset = ShelfAreaFormSet


class ShelfProductAllocRectInline(nested.NestedTabularInline):
    model = ShelfProductAllocRect


class ShelfProductAllocInline(nested.NestedTabularInline):
    model = ShelfProductAlloc
    inlines = [ShelfProductAllocRectInline]


@admin.register(Shelf)
class ShelfAdmin(nested.NestedModelAdmin):
    model = Shelf
    form = ShelfForm
    inlines = [ShelfAreaInline, ShelfProductAllocInline]
    # TODO: 画像ファイル内の座標取得 (jQuery)
