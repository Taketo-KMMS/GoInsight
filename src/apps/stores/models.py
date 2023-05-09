from datetime import datetime
from typing import TYPE_CHECKING

import ulid
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Deferrable, UniqueConstraint

from common.db.models import BaseModel, ULIDField

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager

    from apps.products.models import Product  # noqa: F401


class StoreNameField(models.CharField):
    def validate(self, value: str, model_instance) -> None:
        if value not in self.empty_values:
            return
        if value.endswith("店"):
            raise ValidationError("接尾辞として「店」の文字は利用できません", code="invalid")


class Store(BaseModel):
    id = ULIDField(primary_key=True, editable=False)
    name = StoreNameField("チェーン名", max_length=30)  # type: models.CharField[str, str]

    branches: "RelatedManager[StoreBranch]"

    class Meta:
        verbose_name = verbose_name_plural = "店舗"
        db_table = "stores"

    def __str__(self):
        return self.name


class StoreBranch(BaseModel):
    id = ULIDField(primary_key=True, editable=False)
    name = StoreNameField("支店名", max_length=30)  # type: models.CharField[str, str]
    store = models.ForeignKey(Store, verbose_name="店舗", on_delete=models.CASCADE, related_name="branches")
    store_id: ulid.ULID

    categories: "RelatedManager[StoreCategory]"

    class Meta:
        verbose_name = verbose_name_plural = "支店"
        db_table = "store_branches"

    def __str__(self):
        return f"{self.store} | {self.name}"


class StoreCategory(BaseModel):
    id = ULIDField(primary_key=True, editable=False)
    name = models.CharField("カテゴリー名", max_length=20)
    store_branch = models.ForeignKey(
        StoreBranch, verbose_name="支店", on_delete=models.CASCADE, related_name="categories"
    )
    store_branch_id: ulid.ULID

    shelves: "RelatedManager[Shelf]"

    class Meta:
        verbose_name = verbose_name_plural = "カテゴリー"
        db_table = "store_categories"

    def __str__(self):
        return f"{self.store_branch} | {self.name}"


class Shelf(BaseModel):
    id = ULIDField(primary_key=True, editable=False)
    store_category = models.ForeignKey(
        StoreCategory, verbose_name="カテゴリー", on_delete=models.CASCADE, related_name="shelves"
    )
    store_cateogry_id: ulid.ULID
    start_date = models.DateField("適用開始日")
    end_date = models.DateField("適用終了日", default=datetime.max)
    image = models.FileField("棚画像", blank=True, null=True)
    file = models.FileField("添付ファイル", blank=True, null=True)

    areas: "RelatedManager[ShelfArea]"
    allocs: "RelatedManager[ShelfProductAlloc]"

    class Meta:
        verbose_name = verbose_name_plural = "棚割"
        db_table = "shelves"

    def clean(self) -> None:
        if not self.start_date or not self.end_date:
            return

        qs = self.__class__.objects.filter(end_date__gt=self.start_date, start_date__lt=self.end_date)
        duplicate = qs.first()
        if duplicate is not None:
            start_date = duplicate.start_date.strftime("%Y-%m-%d")
            end_date = duplicate.end_date.strftime("%Y-%m-%d")
            raise ValidationError(f"{start_date}～{end_date}の期間がすでに設定されています")


class ShelfArea(BaseModel):
    id = ULIDField(primary_key=True, editable=False)
    area_number = models.PositiveSmallIntegerField("エリア番号")
    shelf = models.ForeignKey(Shelf, verbose_name="棚割", on_delete=models.CASCADE, related_name="areas")
    shelf_id: ulid.ULID

    class Meta:
        verbose_name = verbose_name_plural = "エリア"
        db_table = "shelf_areas"
        constraints = [
            UniqueConstraint(name="unique_area_number", fields=["area_number", "shelf"], deferrable=Deferrable.DEFERRED)
        ]

    def __str__(self):
        return str(self.area_number)


class ShelfAreaRect(BaseModel):
    shelf_area = models.OneToOneField(ShelfArea, primary_key=True, on_delete=models.CASCADE)
    shelf_area_id: ulid.ULID
    x = models.FloatField("x座標")
    y = models.FloatField("y座標")
    width = models.FloatField("横幅")
    height = models.FloatField("高さ")

    class Meta:
        verbose_name = verbose_name_plural = "エリア矩形"
        db_table = "shelf_area_rects"


class ProductCodeField(models.ForeignKey["Product", "Product"]):
    def get_attname(self):
        return "%s_code" % self.name


class ShelfProductAlloc(BaseModel):
    id = ULIDField(primary_key=True, editable=False)
    area = models.ForeignKey(ShelfArea, verbose_name="エリア", null=True, blank=True, on_delete=models.CASCADE)
    area_id: ulid.ULID | None
    shelf = models.ForeignKey(Shelf, verbose_name="棚割", on_delete=models.CASCADE, related_name="allocs")
    shelf_id: ulid.ULID
    product = ProductCodeField("products.Product", verbose_name="商品", on_delete=models.RESTRICT)
    product_code: str
    # x = models.FloatField("x座標")
    # y = models.FloatField("y座標")
    # width = models.FloatField("矩形幅")
    # height = models.FloatField("矩形高")

    class Meta:
        verbose_name = verbose_name_plural = "商品配置"
        db_table = "shelf_product_allocations"

    def clean(self):
        if self.area_id is not None and self.area.shelf_id != self.shelf_id:
            raise ValidationError("不正なエリアIDが設定されています")
        return super().clean()


class ShelfProductAllocRect(BaseModel):
    alloc_id = models.OneToOneField(ShelfProductAlloc, on_delete=models.CASCADE)

    x = models.FloatField("x座標")
    y = models.FloatField("y座標")
    width = models.FloatField("矩形幅")
    height = models.FloatField("矩形高")

    class Meta:
        verbose_name = verbose_name_plural = "商品配置矩形"
        db_table = "shelf_product_allocation_rects"
