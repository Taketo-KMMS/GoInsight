from typing import Type

from django.apps import AppConfig
from django.contrib.auth import get_permission_codename
from django.db import transaction
from django.db.models import Model, Q
from django.db.models.signals import post_migrate


def create_permission_groups(app_config: AppConfig, *, read=True, write=True, delete=True):
    """読み込み権限、書き込み権限を持つグループを作成する"""
    if not read and not write and not delete:
        raise ValueError("read/write/deleteの一つ以上にTrueを設定してください")

    @transaction.atomic()
    def populate_models(sender: Model, **kwargs):
        from django.apps import apps
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType

        # グループの作成
        reader, _ = Group.objects.get_or_create(name=f"{app_config.verbose_name} 読込") if read else (None, False)
        writer, _ = Group.objects.get_or_create(name=f"{app_config.verbose_name} 変更") if write else (None, False)
        deleter, _ = Group.objects.get_or_create(name=f"{app_config.verbose_name} 削除") if delete else (None, False)
        group, _ = (
            Group.objects.get_or_create(name=app_config.verbose_name) if read and write and delete else (None, False)
        )  # 両方True or 両方False

        # 各モデルに権限を付与する
        model_name: str
        model: Type[Model]
        for model_name, model in apps.all_models[app_config.name].items():
            try:
                content_type = ContentType.objects.get(app_label=app_config.name, model=model_name)
            except ContentType.DoesNotExist:
                continue

            def get_codename(action: str):
                return get_permission_codename(action, model._meta)

            permissions_qs = Permission.objects.filter(content_type=content_type)
            # 権限の付与
            if group:
                group.permissions.add(*permissions_qs)

            if reader:
                reader.permissions.add(*permissions_qs.filter(codename=get_codename("view")))
            if writer:
                writer.permissions.add(
                    *permissions_qs.filter(
                        Q(codename=get_codename("view"))
                        | Q(codename=get_codename("add"))
                        | Q(codename=get_codename("change"))
                    )
                )
            if deleter:
                deleter.permissions.add(
                    *permissions_qs.filter(Q(codename=get_codename("view")) | Q(codename=get_codename("delete")))
                )

    post_migrate.connect(populate_models, sender=app_config)
