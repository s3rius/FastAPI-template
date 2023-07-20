from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Varchar
from piccolo.columns.indexes import IndexMethod

ID = "2022-04-16T17:38:51:672827"
VERSION = "0.74.0"
DESCRIPTION = "Creates dummy model"


async def forwards() -> MigrationManager:
    manager = MigrationManager(
        migration_id=ID, app_name="ptest_db", description=DESCRIPTION
    )

    manager.add_table("DummyModel", tablename="dummy_model")

    manager.add_column(
        table_class_name="DummyModel",
        tablename="dummy_model",
        column_name="name",
        db_column_name="name",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 200,
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    return manager
