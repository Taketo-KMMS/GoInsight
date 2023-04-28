from django.apps import AppConfig


class StoresConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.stores"
    verbose_name = verbose_name_plural = "店舗"

    def ready(self):
        from common.db.models.signals import create_permission_groups

        create_permission_groups(self)
