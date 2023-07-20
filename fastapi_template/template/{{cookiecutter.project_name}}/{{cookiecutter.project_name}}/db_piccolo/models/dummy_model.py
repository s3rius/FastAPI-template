from piccolo.columns import Varchar
from piccolo.table import Table


class DummyModel(Table):
    """Model for demo purpose."""

    name = Varchar(length=200)  # noqa: WPS432
