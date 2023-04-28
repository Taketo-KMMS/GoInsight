import re

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import Group as DjangoGroup
from django.contrib.auth.models import Permission as DjangoPermission
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.db.models import BaseModel

_password_pattern = re.compile(
    r"^(?:"
    r"(?=.*[A-Z])(?=.*[a-z])(?=.*\d)|"
    r"(?=.*[A-Z])(?=.*[a-z])(?=.*[!-/:-@[-`{-~])|"
    r"(?=.*[A-Z])(?=.*\d)(?=.*[!-/:-@[-`{-~])|"
    r"(?=.*[a-z])(?=.*\d)(?=.*[!-/:-@[-`{-~])"
    r")"
    r"[\w!-/:-@[-`{-~]{12,}$"
)


class AdminManager(DjangoUserManager["AdminUser"]):
    def _create_user(self, username, email=None, password=None, *, is_staff=True, **extra_fields) -> "AdminUser":
        # is_staff引数を無効化する
        if not username:
            raise ValueError("The given username must be set")
        if not _password_pattern.match(password or ""):
            raise ValueError("Week Password")
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user


class AdminUser(BaseModel, AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = "username"

    username = models.CharField("ユーザー名", max_length=150, unique=True)
    password = models.CharField(
        _("password"),
        max_length=128,
        validators=(
            RegexValidator(_password_pattern, message="半角英大文字、半角英小文字、半角数字、半角記号のうち3種以上を組み合わせた12文字以上のパスワードを設定してください"),
        ),
    )
    is_active = models.BooleanField("有効", default=True)

    is_staff = True

    objects = AdminManager()

    class Meta:
        db_table = "admin_users"
        verbose_name = verbose_name_plural = "システム管理者"

    def __str__(self) -> str:
        return self.username


class AdminGroup(DjangoGroup):
    class Meta:
        proxy = True
        managed = False
        verbose_name = verbose_name_plural = "システム管理グループ"


class AdminPermission(DjangoPermission):
    class Meta:
        proxy = True
        managed = False
        verbose_name = verbose_name_plural = "システム権限"

    def __str__(self) -> str:
        return self.name
