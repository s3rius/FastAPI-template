from tortoise import fields, models


class DummyModel(models.Model):
    """Model for demo purpose."""

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=200)  # noqa: WPS432

    def __str__(self) -> str:
        return self.name
