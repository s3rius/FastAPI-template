from piccolo.table import Table
from piccolo.columns import Varchar


class DummyModel(Table):
    """Model for demo purpose."""

    name = Varchar(length=200)  # noqa: WPS432
