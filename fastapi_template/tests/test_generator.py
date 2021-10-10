from typing import Optional
from fastapi_template.tests.utils import run_default_check
import pytest

from fastapi_template.input_model import ORM, BuilderContext, DatabaseType, DB_INFO


def init_context(
    context: BuilderContext, db: DatabaseType, orm: Optional[ORM]
) -> BuilderContext:
    context.db = db
    context.db_info = DB_INFO[db]
    context.orm = orm

    context.enable_migrations = db != DatabaseType.none
    context.add_dummy = db != DatabaseType.none    

    return context


def test_default_without_db(default_context: BuilderContext):
    run_default_check(init_context(default_context, DatabaseType.none, None))


@pytest.mark.parametrize(
    "db",
    [
        DatabaseType.postgresql,
        DatabaseType.sqlite,
        DatabaseType.mysql,
    ],
)
@pytest.mark.parametrize("orm", [ORM.sqlalchemy, ORM.tortoise, ORM.ormar])
def test_default_with_db(default_context: BuilderContext, db: DatabaseType, orm: ORM):
    run_default_check(init_context(default_context, db, orm))


@pytest.mark.parametrize("orm", [ORM.sqlalchemy, ORM.tortoise, ORM.ormar])
def test_without_routers(default_context: BuilderContext, orm: ORM):
    context = init_context(default_context, DatabaseType.postgresql, orm)
    context.enable_routers = False
    run_default_check(context)


@pytest.mark.parametrize("orm", [ORM.sqlalchemy, ORM.tortoise, ORM.ormar])
def test_without_migrations(default_context: BuilderContext, orm: ORM):
    context = init_context(default_context, DatabaseType.postgresql, orm)
    context.enable_migrations = False
    run_default_check(context)


def test_with_selfhosted_swagger(default_context: BuilderContext):
    default_context.self_hosted_swagger = True
    run_default_check(default_context)


@pytest.mark.parametrize("orm", [ORM.sqlalchemy, ORM.tortoise, ORM.ormar])
def test_without_dummy(default_context: BuilderContext, orm: ORM):
    context = init_context(default_context, DatabaseType.postgresql, orm)
    context.add_dummy = False
    run_default_check(context)


def test_redis(default_context: BuilderContext):
    default_context.enable_redis = True
    run_default_check(default_context)
