from datetime import date
from typing import TYPE_CHECKING

import ulid
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.db import models

from common.db.models import BaseModel, ULIDField

if TYPE_CHECKING:
    from apps.researches.models import Project  # noqa: F401


class ClientUser(BaseModel):
    id = ULIDField(primary_key=True, editable=False)
    display_name = models.CharField(verbose_name="ユーザー名", max_length=63)
    email = models.EmailField(verbose_name="メールアドレス", max_length=255)
    # TODO: パスワード生成ロジック
    hashed_password = models.CharField(verbose_name="パスワード", max_length=255)
    group = models.ForeignKey["ClientGroup", "ClientGroup"](
        "ClientGroup", verbose_name="グループ", on_delete=models.RESTRICT
    )
    group_id: ulid.ULID
    is_manager = models.BooleanField(verbose_name="グループ管理者")

    class Meta:
        verbose_name = verbose_name_plural = "クライアントユーザー"
        db_table = "client_users"

    def __str__(self):
        return self.display_name

    def clean(self):
        qs = self.__class__.objects.filter(group_id=self.group_id).exclude(pk=self.pk)
        if self.is_manager is qs.filter(is_manager=True).exists():
            raise ValidationError("グループには管理者を1名設定してください")
        return super().clean()


def _one_year_after():
    return date.today() + relativedelta(years=1)


class ClientGroup(BaseModel):
    id = ULIDField(primary_key=True, editable=False)
    group_name = models.CharField(verbose_name="グループID", max_length=20)
    display_name = models.CharField(verbose_name="グループ名", max_length=30)
    expiration_date = models.DateField(verbose_name="有効期限", default=_one_year_after)
    is_superuser = models.BooleanField(verbose_name="管理者権限", default=False)

    projects = models.ManyToManyField(
        "researches.Project", verbose_name="プロジェクト", through="ClientGroupPermission", blank=True
    )

    class Meta:
        verbose_name = verbose_name_plural = "クライアントグループ"
        db_table = "client_groups"

    def __str__(self):
        return self.display_name


class ClientGroupPermission(BaseModel):
    group = models.ForeignKey(ClientGroup, on_delete=models.CASCADE)
    group_id: ulid.ULID
    project = models.ForeignKey["Project", "Project"]("researches.Project", on_delete=models.CASCADE)
    project_id: ulid.ULID

    class Meta:
        db_table = "client_group_permissions"
