from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey, TreeManager

from common.db.models import BaseModel

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager


class ProductMaker(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField("メーカー名", max_length=50)

    class Meta:
        verbose_name = verbose_name_plural = "商品メーカー"
        db_table = "product_makers"

    def __str__(self):
        return self.name


class ProductCategory(MPTTModel, BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField("カテゴリー名", max_length=20)
    parent: "models.ForeignKey[ProductCategory, ProductCategory]" = TreeForeignKey(
        "self", verbose_name="親カテゴリー", null=True, blank=True, on_delete=models.CASCADE, related_name="children"
    )
    parent_id: int | None

    objects: "TreeManager | models.Manager[ProductCategory]"
    children: "TreeManager | RelatedManager[ProductCategory]"

    MAX_TREE_DEPTH = 3

    class Meta:
        verbose_name = verbose_name_plural = "商品カテゴリー"
        db_table = "product_categories"

    def clean(self):
        parent = self.parent
        if parent is not None and parent.get_level() >= self.MAX_TREE_DEPTH:
            raise ValidationError(f"カテゴリーの最大階層は{self.MAX_TREE_DEPTH + 1}です")

    def __str__(self):
        return self.name

    @property
    def fullname(self):
        return self.name if self.parent_id is None else f"{self.parent.fullname} > {self.name}"


class Product(BaseModel):
    # POPやQRは大文字英語+yyyymmddhhmm
    code = models.CharField("商品コード", primary_key=True, max_length=14)
    name = models.CharField("商品名", max_length=100, db_column="name")
    maker = models.ForeignKey(ProductMaker, verbose_name="メーカー", null=True, blank=True, on_delete=models.CASCADE)
    maker_id: int | None
    category = models.ForeignKey(ProductCategory, verbose_name="カテゴリー", null=True, blank=True, on_delete=models.CASCADE)
    category_id: int | None

    class Meta:
        verbose_name = verbose_name_plural = "商品"
        db_table = "products"

    def __str__(self):
        return self.name
