# TODO: イベントCSVインポートエクスポートページ

from typing import Sequence

from django.contrib import admin

from .models import AreaEvent, BaseEvent, FrameEvent, OptionalEvent, ProductEvent


# TODO: 期間も絞り込みはいる
class EventAdminBase(admin.ModelAdmin):
    list_select_related: Sequence[str] = ("customer__research", "customer__research__project")

    def research(self, obj: BaseEvent):
        return obj.customer.research.name or obj.customer.research.id

    research.short_description = "調査"  # type: ignore
    research.admin_order_field = ("customer__research__name", "customer__research__id")  # type: ignore

    def project(self, obj: BaseEvent):
        return obj.customer.research.project.name or obj.customer.research.project.id

    project.short_description = "プロジェクト"  # type: ignore
    project.admin_order_field = ("customer__research__project__name", "customer__research__project__id")  # type: ignore


@admin.register(FrameEvent)
class FrameEventAdmin(EventAdminBase):
    list_display = ("id", "project", "research", "customer", "in_time", "out_time")

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_change_permission(self, *args, **kwargs):
        return False


@admin.register(AreaEvent)
class AreaEventAdmin(EventAdminBase):
    list_display = ("id", "project", "research", "customer", "area_number", "in_time", "out_time")
    list_select_related = [*EventAdminBase.list_select_related, "area"]

    def area_number(self, obj: AreaEvent):
        return obj.area.area_number

    area_number.short_description = "エリア"  # type: ignore
    area_number.admin_order_field = "area__area_number"  # type: ignore

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_change_permission(self, *args, **kwargs):
        return False


@admin.register(ProductEvent)
class ProductEventAdmin(EventAdminBase):
    # TODO: JANコード完全一致、商品名のサジェスト、での絞り込み
    list_display = (
        "id",
        "project",
        "research",
        "customer",
        "product_code",
        "product_name",
        "product_maker",
        "buy_flag",
        "touch_time",
    )
    list_select_related = [*EventAdminBase.list_select_related, "allocation__product", "allocation__product__maker"]

    def product_code(self, obj: ProductEvent):
        return obj.allocation.product.code

    product_code.short_description = "商品コード"  # type: ignore
    product_code.admin_order_field = "allocation__product__code"  # type: ignore

    def product_name(self, obj: ProductEvent):
        return obj.allocation.product.name

    product_name.short_description = "商品名"  # type: ignore
    product_name.admin_order_field = "allocation__product__name"  # type: ignore

    def product_maker(self, obj: ProductEvent):
        maker = obj.allocation.product.maker
        return maker and maker.name

    product_maker.short_description = "メーカー"  # type: ignore
    product_maker.admin_order_field = "allocation__product__maker__name"  # type: ignore

    def has_add_permission(self, *args, **kwags):
        return False

    def has_change_permission(self, *args, **kwargs):
        return False


@admin.register(OptionalEvent)
class OptionalEventAdmin(EventAdminBase):
    list_display = ("id", "project", "research", "customer", "event_type", "event_time")

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_change_permission(self, *args, **kwargs):
        return False
