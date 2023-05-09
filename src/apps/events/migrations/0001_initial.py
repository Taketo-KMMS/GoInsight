# Generated by Django 4.2 on 2023-05-09 04:59

import common.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("researches", "0001_initial"),
        ("stores", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "created_at",
                    django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name="作成日"),
                ),
                ("id", common.db.models.fields.ULIDField(editable=False, primary_key=True, serialize=False)),
                ("gender", models.PositiveSmallIntegerField(choices=[(1, "男性"), (2, "女性")], verbose_name="性別")),
                (
                    "age",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "0代"),
                            (10, "10代"),
                            (20, "20代"),
                            (30, "30代"),
                            (40, "40代"),
                            (50, "50代"),
                            (60, "60代"),
                            (70, "70代"),
                        ],
                        verbose_name="年齢",
                    ),
                ),
                ("date", models.DateField(verbose_name="発生日")),
                ("research", models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to="researches.research")),
            ],
            options={
                "verbose_name": "顧客",
                "verbose_name_plural": "顧客",
                "db_table": "customers",
            },
        ),
        migrations.CreateModel(
            name="ProductEvent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "created_at",
                    django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name="作成日"),
                ),
                ("touch_time", models.TimeField(verbose_name="接触発生日時")),
                ("buy_flag", models.BooleanField(verbose_name="購入フラグ")),
                (
                    "allocation",
                    models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to="stores.shelfproductalloc"),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="events.customer", verbose_name="顧客"
                    ),
                ),
            ],
            options={
                "verbose_name": "接触購入イベント",
                "verbose_name_plural": "接触購入イベント",
                "db_table": "product_events",
            },
        ),
        migrations.CreateModel(
            name="OptionalEvent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "created_at",
                    django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name="作成日"),
                ),
                ("event_type", models.SmallIntegerField(choices=[], verbose_name="イベント種別")),
                ("event_time", models.TimeField(verbose_name="イベント発生日時")),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="events.customer", verbose_name="顧客"
                    ),
                ),
            ],
            options={
                "verbose_name": "その他イベント",
                "verbose_name_plural": "その他イベント",
                "db_table": "optional_events",
            },
        ),
        migrations.CreateModel(
            name="FrameEvent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "created_at",
                    django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name="作成日"),
                ),
                ("in_time", models.TimeField(verbose_name="フレームイン発生日時")),
                ("out_time", models.TimeField(verbose_name="フレームアウト発生日時")),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="events.customer", verbose_name="顧客"
                    ),
                ),
            ],
            options={
                "verbose_name": "フレームイベント",
                "verbose_name_plural": "フレームイベント",
                "db_table": "frame_events",
            },
        ),
        migrations.CreateModel(
            name="CustomerAttr",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "created_at",
                    django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name="作成日"),
                ),
                (
                    "attribute",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT, to="researches.projectcustomerattr"
                    ),
                ),
                ("customer", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="events.customer")),
            ],
            options={
                "verbose_name": "顧客オプション属性",
                "verbose_name_plural": "顧客オプション属性",
                "db_table": "customer_attributes",
            },
        ),
        migrations.CreateModel(
            name="AreaEvent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "created_at",
                    django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name="作成日"),
                ),
                ("in_time", models.TimeField(verbose_name="エリアイン発生日時")),
                ("out_time", models.TimeField(verbose_name="エリアアウト発生日時")),
                (
                    "area",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT, to="stores.shelfarea", verbose_name="エリア"
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="events.customer", verbose_name="顧客"
                    ),
                ),
            ],
            options={
                "verbose_name": "エリアイベント",
                "verbose_name_plural": "エリアイベント",
                "db_table": "area_events",
            },
        ),
    ]
