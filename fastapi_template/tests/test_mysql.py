from fastapi_template.tests.utils import run_default_check
import pytest

from fastapi_template.input_model import BuilderContext, DatabaseType, DB_INFO


@pytest.fixture()
def mysql_context(defautl_context: BuilderContext) -> BuilderContext:
    defautl_context.db = DatabaseType.mysql
    defautl_context.db_info = DB_INFO[DatabaseType.mysql]

    return defautl_context


@pytest.mark.mysql
def test_default_mysql(mysql_context: BuilderContext):
    run_default_check(mysql_context)


@pytest.mark.mysql
def test_mysql_without_routers(mysql_context: BuilderContext):
    mysql_context.enable_routers = False
    run_default_check(mysql_context)


@pytest.mark.mysql
def test_mysql_without_alembic(mysql_context: BuilderContext):
    mysql_context.enable_alembic = False
    run_default_check(mysql_context)


@pytest.mark.mysql
def test_mysql_with_selfhosted_swagger(mysql_context: BuilderContext):
    mysql_context.self_hosted_swagger = True
    run_default_check(mysql_context)


@pytest.mark.mysql
def test_mysql_without_dummy(mysql_context: BuilderContext):
    mysql_context.add_dummy = False
    run_default_check(mysql_context)


@pytest.mark.mysql
def test_mysql_and_redis(mysql_context: BuilderContext):
    mysql_context.enable_redis = True
    run_default_check(mysql_context)
