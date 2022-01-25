from piccolo.columns import Varchar
from piccolo.table import Table


class DummyModel(Table):
    name = Varchar(length=200)
