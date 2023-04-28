from datetime import datetime
from typing import TYPE_CHECKING

import ulid
from django.db import models

from common.db.models import CreatedAtModel, ULIDField

if TYPE_CHECKING:
    from apps.researches.models import ProjectCustomerAttr, Research  # noqa: F401
    from apps.stores.models import ShelfArea, ShelfProductAlloc  # noqa: F401


class Customer(CreatedAtModel):
    class GenderChoices(models.IntegerChoices):
        MALE = 1, "男性"
        FEMALE = 2, "女性"

    class AgeChoices(models.IntegerChoices):
        AGE_00 = 0, "0代"
        AGE_10 = 10, "10代"
        AGE_20 = 20, "20代"
        AGE_30 = 30, "30代"
        AGE_40 = 40, "40代"
        AGE_50 = 50, "50代"
        AGE_60 = 60, "60代"
        AGE_70 = 70, "70代"

    id = ULIDField(primary_key=True, editable=False)
    gender = models.PositiveSmallIntegerField("性別", choices=GenderChoices.choices)
    age = models.PositiveSmallIntegerField("年齢", choices=AgeChoices.choices)
    date = models.DateField("発生日")
    research = models.ForeignKey["Research", "Research"]("researches.Research", on_delete=models.RESTRICT)
    research_id: ulid.ULID

    class Meta:
        verbose_name = verbose_name_plural = "顧客"
        db_table = "customers"


class CustomerAttr(CreatedAtModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    customer_id: ulid.ULID
    attribute = models.ForeignKey["ProjectCustomerAttr", "ProjectCustomerAttr"](
        "researches.ProjectCustomerAttr", on_delete=models.RESTRICT
    )
    attribute_id: ulid.ULID

    class Meta:
        verbose_name = verbose_name_plural = "顧客オプション属性"
        db_table = "customer_attributes"


class BaseEvent(CreatedAtModel):
    customer = models.ForeignKey(Customer, verbose_name="顧客", on_delete=models.CASCADE)
    customer_id: ulid.ULID

    class Meta:
        abstract = True


class FrameEvent(BaseEvent):
    in_time = models.TimeField("フレームイン発生日時")
    out_time = models.TimeField("フレームアウト発生日時")

    class Meta:
        verbose_name = verbose_name_plural = "フレームイベント"
        db_table = "frame_events"

    def __str__(self):
        return self.customer.research.project

    @property
    def in_datetime(self):
        return datetime.combine(self.customer.date, self.in_time)

    @property
    def out_datetime(self):
        return datetime.combine(self.customer.date, self.out_time)


class AreaEvent(BaseEvent):
    area = models.ForeignKey["ShelfArea", "ShelfArea"](
        "stores.ShelfArea", verbose_name="エリア", on_delete=models.RESTRICT
    )
    area_id: ulid.ULID
    in_time = models.TimeField("エリアイン発生日時")
    out_time = models.TimeField("エリアアウト発生日時")

    class Meta:
        verbose_name = verbose_name_plural = "エリアイベント"
        db_table = "area_events"

    @property
    def in_datetime(self):
        return datetime.combine(self.customer.date, self.in_time)

    @property
    def out_datetime(self):
        return datetime.combine(self.customer.date, self.in_time)


class ProductEvent(BaseEvent):
    allocation = models.ForeignKey["ShelfProductAlloc", "ShelfProductAlloc"](
        "stores.ShelfProductAlloc", on_delete=models.RESTRICT
    )
    allocation_id: ulid.ULID
    touch_time = models.TimeField("接触発生日時")
    buy_flag = models.BooleanField("購入フラグ")

    class Meta:
        verbose_name = verbose_name_plural = "接触購入イベント"
        db_table = "product_events"

    @property
    def touch_datetime(self):
        return datetime.combine(self.customer.date, self.touch_time)


class OptionalEvent(BaseEvent):
    class EventType(models.IntegerChoices):
        pass

    event_type = models.SmallIntegerField("イベント種別", choices=EventType.choices)
    event_time = models.TimeField("イベント発生日時")

    @property
    def event_datetime(self):
        return datetime.combine(self.customer.date, self.event_time)

    class Meta:
        verbose_name = verbose_name_plural = "その他イベント"
        db_table = "optional_events"
