from typing import TYPE_CHECKING

import ulid
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Deferrable, UniqueConstraint

from common.db.models import BaseModel, ULIDField

if TYPE_CHECKING:
    from apps.stores.models import Shelf, StoreCategory  # noqa: F401


class Project(BaseModel):
    id = ULIDField(primary_key=True, editable=False)
    name = models.CharField("プロジェクト識別名", max_length=50, null=True, blank=True)
    store_category = models.ForeignKey["StoreCategory", "StoreCategory"](
        "stores.StoreCategory", verbose_name="カテゴリー", on_delete=models.RESTRICT
    )
    store_category_id: ulid.ULID

    class Meta:
        verbose_name = verbose_name_plural = "プロジェクト"
        db_table = "projects"

    def __str__(self):
        return self.name or str(self.id)


class Research(BaseModel):
    id = ULIDField(primary_key=True, editable=False)
    name = models.CharField("期間識別名", max_length=20, null=True, blank=True)
    project = models.ForeignKey(Project, verbose_name="プロジェクト", on_delete=models.CASCADE)
    project_id: ulid.ULID
    shelf = models.ForeignKey["Shelf", "Shelf"]("stores.Shelf", verbose_name="棚割", on_delete=models.RESTRICT)
    shelf_id: ulid.ULID
    start_date = models.DateField("調査開始日")
    end_date = models.DateField("調査終了日")

    class Meta:
        verbose_name = verbose_name_plural = "調査期間"
        db_table = "researches"

    def clean(self) -> None:
        qs = self.__class__.objects.filter(end_date__gt=self.start_date, start_date__lt=self.end_date)
        duplicate = qs.first()
        if duplicate is not None:
            start_date = duplicate.start_date.strftime("%Y-%m-%d")
            end_date = duplicate.end_date.strftime("%Y-%m-%d")
            raise ValidationError(f"{start_date}～{end_date}の期間がすでに設定されています")


class ProjectCustomerAttr(BaseModel):
    id = ULIDField(primary_key=True, editable=False)
    project = models.ForeignKey(Project, verbose_name="プロジェクト", on_delete=models.CASCADE)
    project_id: ulid.ULID
    name = models.CharField("顧客属性名", max_length=10)
    order = models.PositiveSmallIntegerField("表示順序")

    class Meta:
        verbose_name = verbose_name_plural = "プロジェクト固有顧客属性"
        db_table = "project_customer_attributes"
        constraints = [
            UniqueConstraint(name="unique_attr_name", fields=("project", "name"), deferrable=Deferrable.DEFERRED),
            UniqueConstraint(name="unique_attr_order", fields=("project", "order"), deferrable=Deferrable.DEFERRED),
        ]
