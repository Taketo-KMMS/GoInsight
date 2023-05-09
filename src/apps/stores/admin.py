from django.contrib import admin
from nested_admin import nested

from .forms import ShelfForm, ShelfProductAllocForm
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
    list_select_related = ("store_branch", "store_branch__store")


class StoreBranchInline(nested.NestedStackedInline):
    extra = 1
    model = StoreBranch
    inlines = [StoreCategoryInline]
    list_select_related = ("store",)


@admin.register(Store)
class StoreAdmin(nested.NestedModelAdmin):
    inlines = [StoreBranchInline]


class ShelfAreaRectInline(nested.NestedTabularInline):
    model = ShelfAreaRect


class ShelfAreaInline(nested.NestedStackedInline):
    extra = 1
    model = ShelfArea
    inlines = [ShelfAreaRectInline]


class ShelfProductAllocRectInline(nested.NestedTabularInline):
    extra = 0
    model = ShelfProductAllocRect


class ShelfProductAllocInline(nested.NestedTabularInline):
    extra = 1
    model = ShelfProductAlloc
    form = ShelfProductAllocForm
    inlines = [ShelfProductAllocRectInline]


@admin.register(Shelf)
class ShelfAdmin(nested.NestedModelAdmin):
    model = Shelf
    form = ShelfForm
    inlines = [ShelfAreaInline, ShelfProductAllocInline]
    # TODO: 画像ファイル内の座標取得 (jQuery)
