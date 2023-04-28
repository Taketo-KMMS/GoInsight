# Generated by Django 4.2 on 2023-04-28 09:13

import apps.clients.models
import common.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("researches", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ClientGroup",
            fields=[
                (
                    "created_at",
                    django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name="作成日"),
                ),
                (
                    "updated_at",
                    django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name="更新日"),
                ),
                ("id", common.db.models.fields.ULIDField(editable=False, primary_key=True, serialize=False)),
                ("group_name", models.CharField(max_length=20, verbose_name="グループID")),
                ("display_name", models.CharField(max_length=30, verbose_name="グループ名")),
                ("expiration_date", models.DateField(default=apps.clients.models._one_year_after, verbose_name="有効期限")),
                ("is_superuser", models.BooleanField(default=False, verbose_name="管理者権限")),
            ],
            options={
                "verbose_name": "クライアントグループ",
                "verbose_name_plural": "クライアントグループ",
                "db_table": "client_groups",
            },
        ),
        migrations.CreateModel(
            name="ClientUser",
            fields=[
                (
                    "created_at",
                    django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name="作成日"),
                ),
                (
                    "updated_at",
                    django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name="更新日"),
                ),
                ("id", common.db.models.fields.ULIDField(editable=False, primary_key=True, serialize=False)),
                ("display_name", models.CharField(max_length=63, verbose_name="ユーザー名")),
                ("email", models.EmailField(max_length=255, verbose_name="メールアドレス")),
                ("hashed_password", models.CharField(max_length=255, verbose_name="パスワード")),
                ("is_manager", models.BooleanField(verbose_name="グループ管理者")),
                (
                    "group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT, to="clients.clientgroup", verbose_name="グループ"
                    ),
                ),
            ],
            options={
                "verbose_name": "クライアントユーザー",
                "verbose_name_plural": "クライアントユーザー",
                "db_table": "client_users",
            },
        ),
        migrations.CreateModel(
            name="ClientGroupPermission",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "created_at",
                    django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name="作成日"),
                ),
                (
                    "updated_at",
                    django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name="更新日"),
                ),
                ("group", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="clients.clientgroup")),
                ("project", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="researches.project")),
            ],
            options={
                "db_table": "client_group_permissions",
            },
        ),
        migrations.AddField(
            model_name="clientgroup",
            name="projects",
            field=models.ManyToManyField(
                blank=True, through="clients.ClientGroupPermission", to="researches.project", verbose_name="プロジェクト"
            ),
        ),
    ]