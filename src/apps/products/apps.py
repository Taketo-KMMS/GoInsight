from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.products"
    verbose_name = verbose_name_plural = "商品"

    def ready(self):
        from common.db.models.signals import create_permission_groups

        create_permission_groups(self)
