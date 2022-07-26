from typing import Optional
from fastapi_template.tests.utils import run_default_check
import pytest

from fastapi_template.input_model import (
    ORM,
    APIType,
    BuilderContext,
    DatabaseType,
    DB_INFO,
    SUPPORTED_ORMS,
)


def init_context(
    context: BuilderContext,
    db: DatabaseType,
    orm: Optional[ORM],
    api: Optional[APIType] = None,
) -> BuilderContext:
    context.db = db
    context.db_info = DB_INFO[db]
    context.orm = orm

    if api is not None:
        context.api_type = api

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
@pytest.mark.parametrize(
    "orm",
    [
        ORM.sqlalchemy,
        ORM.tortoise,
        ORM.ormar,
        ORM.piccolo,
    ],
)
def test_default_with_db(default_context: BuilderContext, db: DatabaseType, orm: ORM):
    if orm not in SUPPORTED_ORMS[db]:
        return
    run_default_check(init_context(default_context, db, orm))


@pytest.mark.parametrize("api", [APIType.rest, APIType.graphql])
@pytest.mark.parametrize(
    "orm",
    [
        ORM.sqlalchemy,
        ORM.tortoise,
        ORM.ormar,
        ORM.piccolo,
    ],
)
def test_default_for_apis(default_context: BuilderContext, orm: ORM, api: APIType):
    run_default_check(init_context(default_context, DatabaseType.postgresql, orm, api))


@pytest.mark.parametrize(
    "orm",
    [
        ORM.psycopg,
    ],
)
def test_pg_drivers(default_context: BuilderContext, orm: ORM):
    run_default_check(init_context(default_context, DatabaseType.postgresql, orm))


@pytest.mark.parametrize(
    "orm", [ORM.sqlalchemy, ORM.tortoise, ORM.ormar, ORM.psycopg, ORM.piccolo]
)
def test_without_routers(default_context: BuilderContext, orm: ORM):
    context = init_context(default_context, DatabaseType.postgresql, orm)
    context.enable_routers = False
    run_default_check(context)


@pytest.mark.parametrize("orm", [ORM.sqlalchemy, ORM.tortoise, ORM.ormar, ORM.piccolo])
def test_without_migrations(default_context: BuilderContext, orm: ORM):
    context = init_context(default_context, DatabaseType.postgresql, orm)
    context.enable_migrations = False
    run_default_check(context)


def test_with_selfhosted_swagger(default_context: BuilderContext):
    default_context.self_hosted_swagger = True
    run_default_check(default_context)


@pytest.mark.parametrize(
    "orm", [ORM.sqlalchemy, ORM.tortoise, ORM.ormar, ORM.psycopg, ORM.piccolo]
)
def test_without_dummy(default_context: BuilderContext, orm: ORM):
    context = init_context(default_context, DatabaseType.postgresql, orm)
    context.add_dummy = False
    run_default_check(context)


@pytest.mark.parametrize("api", [APIType.rest, APIType.graphql])
def test_redis(default_context: BuilderContext, api: APIType):
    default_context.enable_redis = True
    default_context.api_type = api
    run_default_check(default_context)


@pytest.mark.parametrize("api", [APIType.rest, APIType.graphql])
def test_rmq(default_context: BuilderContext, api: APIType):
    default_context.enable_rmq = True
    default_context.api_type = api
    run_default_check(default_context)


def test_telemetry_pre_commit(default_context: BuilderContext):
    default_context.enable_rmq = True
    default_context.enable_redis = True
    default_context.prometheus_enabled = True
    default_context.otlp_enabled = True
    default_context.sentry_enabled = True
    default_context.enable_loguru = True
    run_default_check(default_context, without_pytest=True)

# @pytest.mark.parametrize("api", [APIType.rest, APIType.graphql])
# def test_kafka(default_context: BuilderContext, api: APIType):
#     default_context.enable_kafka = True
#     default_context.api_type = api
#     run_default_check(default_context)
