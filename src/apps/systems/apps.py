from django.apps import AppConfig


class SystemsConfig(AppConfig):
    name = "apps.systems"
    verbose_name = verbose_name_plural = "システム"

    def ready(self):
        from common.db.models.signals import create_permission_groups

        create_permission_groups(self)
