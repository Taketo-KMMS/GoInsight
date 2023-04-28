from django.apps import AppConfig


class EventsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.events"
    verbose_name = verbose_name_plural = "イベント"

    def ready(self):
        from common.db.models.signals import create_permission_groups

        create_permission_groups(self, write=False)
