from fastapi_template.tests.utils import run_default_check
import pytest

from fastapi_template.input_model import BuilderContext, DatabaseType, DB_INFO


@pytest.fixture()
def sqlite_context(defautl_context: BuilderContext) -> BuilderContext:
    defautl_context.db = DatabaseType.sqlite
    defautl_context.db_info = DB_INFO[DatabaseType.sqlite]

    return defautl_context


@pytest.mark.sqlite
def test_default_sqlite(sqlite_context: BuilderContext):
    run_default_check(sqlite_context)


@pytest.mark.sqlite
def test_sqlite_without_routers(sqlite_context: BuilderContext):
    sqlite_context.enable_routers = False
    run_default_check(sqlite_context)


@pytest.mark.sqlite
def test_sqlite_without_alembic(sqlite_context: BuilderContext):
    sqlite_context.enable_alembic = False
    run_default_check(sqlite_context)


@pytest.mark.sqlite
def test_sqlite_with_selfhosted_swagger(sqlite_context: BuilderContext):
    sqlite_context.self_hosted_swagger = True
    run_default_check(sqlite_context)


@pytest.mark.sqlite
def test_sqlite_without_dummy(sqlite_context: BuilderContext):
    sqlite_context.add_dummy = False
    run_default_check(sqlite_context)


@pytest.mark.sqlite
def test_sqlite_and_redis(sqlite_context: BuilderContext):
    sqlite_context.enable_redis = True
    run_default_check(sqlite_context)
