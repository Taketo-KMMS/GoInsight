import ulid
from django.core.validators import MinLengthValidator
from django.db import models
from django.db.backends.base.base import BaseDatabaseWrapper


class ULIDField(models.Field):
    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 26
        kwargs["default"] = ulid.new
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_length"]
        del kwargs["default"]
        return name, path, args, kwargs

    def db_type(self, connection):
        return "char(26)"

    def from_db_value(self, value, expression, connection):
        if value is not None:
            return ulid.from_str(value)
        return value

    def to_python(self, value):
        if isinstance(value, ulid.ULID):
            return value
        if value is not None:
            return ulid.from_str(value)
        return value

    def get_prep_value(self, value):
        if isinstance(value, ulid.ULID):
            return str(value)
        return value


class FixedCharField(models.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators.append(MinLengthValidator(self.max_length))

    def db_type(self, connection: BaseDatabaseWrapper) -> str:
        return f"CHAR({self.max_length})"
