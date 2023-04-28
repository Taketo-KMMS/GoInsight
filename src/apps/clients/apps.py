from django.apps import AppConfig


class ClientsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.clients"
    verbose_name = verbose_name_plural = "クライアント"

    def ready(self):
        from common.db.models.signals import create_permission_groups

        create_permission_groups(self)
