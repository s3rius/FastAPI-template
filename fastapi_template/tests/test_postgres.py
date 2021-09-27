from fastapi_template.tests.utils import run_default_check
import pytest

from fastapi_template.input_model import BuilderContext, DatabaseType, DB_INFO


@pytest.fixture()
def pg_context(defautl_context: BuilderContext) -> BuilderContext:
    defautl_context.db = DatabaseType.postgresql
    defautl_context.db_info = DB_INFO[DatabaseType.postgresql]

    return defautl_context


@pytest.mark.pg
def test_default_pg(pg_context: BuilderContext):
    run_default_check(pg_context)


@pytest.mark.pg
def test_pg_without_routers(pg_context: BuilderContext):
    pg_context.enable_routers = False
    run_default_check(pg_context)


@pytest.mark.pg
def test_pg_without_alembic(pg_context: BuilderContext):
    pg_context.enable_alembic = False
    run_default_check(pg_context)


@pytest.mark.pg
def test_pg_with_selfhosted_swagger(pg_context: BuilderContext):
    pg_context.self_hosted_swagger = True
    run_default_check(pg_context)


@pytest.mark.pg
def test_pg_without_dummy(pg_context: BuilderContext):
    pg_context.add_dummy = False
    run_default_check(pg_context)


@pytest.mark.pg
def test_pg_and_redis(pg_context: BuilderContext):
    pg_context.enable_redis = True
    run_default_check(pg_context)
