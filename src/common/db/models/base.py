from django.db import models
from django_extensions.db.models import CreationDateTimeField, ModificationDateTimeField


class CreatedAtModel(models.Model):
    created_at = CreationDateTimeField(verbose_name="作成日")

    class Meta:
        abstract = True


class UpdatedAtModel(models.Model):
    updated_at = ModificationDateTimeField(verbose_name="更新日")

    class Meta:
        abstract = True


class BaseModel(CreatedAtModel, UpdatedAtModel):
    class Meta:
        abstract = True
