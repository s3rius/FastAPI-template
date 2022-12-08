from typing import Optional
from fastapi_template.tests.utils import run_default_check
import pytest

from fastapi_template.input_model import BuilderContext
from fastapi_template.cli import db_menu


def init_context(
    context: BuilderContext,
    db: str,
    orm: Optional[str],
    api: Optional[str] = None,
) -> BuilderContext:
    db_info = None
    for entry in db_menu.entries:
        if entry.code == db:
            db_info = entry.additional_info.dict()
    if db_info is None:
        raise ValueError(f"Unknown database: {db}")

    context.db = db
    context.db_info = db_info
    context.orm = orm

    if api is not None:
        context.api_type = api

    context.enable_migrations = db != "none"
    context.add_dummy = db != "none"

    return context


def test_default_without_db(default_context: BuilderContext):
    run_default_check(init_context(default_context, "none", None))


@pytest.mark.parametrize(
    "db",
    [
        "postgresql",
        "sqlite",
        "mysql",
    ],
)
@pytest.mark.parametrize(
    "orm",
    [
        "sqlalchemy",
        "tortoise",
        "ormar",
        "piccolo",
    ],
)
def test_default_with_db(default_context: BuilderContext, db: str, orm: str):
    if orm == "piccolo" and db == "mysql":
        return
    run_default_check(init_context(default_context, db, orm))


@pytest.mark.parametrize("api", ["rest", "graphql"])
@pytest.mark.parametrize(
    "orm",
    [
        "sqlalchemy",
        "tortoise",
        "ormar",
        "piccolo",
    ],
)
def test_default_for_apis(default_context: BuilderContext, orm: str, api: str):
    run_default_check(init_context(default_context, "postgresql", orm, api))


@pytest.mark.parametrize(
    "orm",
    [
        "psycopg",
    ],
)
def test_pg_drivers(default_context: BuilderContext, orm: str):
    run_default_check(init_context(default_context, "postgresql", orm))


@pytest.mark.parametrize(
    "orm",
    [
        "sqlalchemy",
        "tortoise",
        "ormar",
        "psycopg",
        "piccolo",
    ],
)
def test_without_routers(default_context: BuilderContext, orm: str):
    context = init_context(default_context, "postgresql", orm)
    context.enable_routers = False
    run_default_check(context)


@pytest.mark.parametrize(
    "orm",
    [
        "sqlalchemy",
        "tortoise",
        "ormar",
        "piccolo",
    ],
)
def test_without_migrations(default_context: BuilderContext, orm: str):
    context = init_context(default_context, "postgresql", orm)
    context.enable_migrations = False
    run_default_check(context)


def test_with_selfhosted_swagger(default_context: BuilderContext):
    default_context.self_hosted_swagger = True
    run_default_check(default_context)


@pytest.mark.parametrize(
    "orm",
    [
        "sqlalchemy",
        "tortoise",
        "ormar",
        "psycopg",
        "piccolo",
    ],
)
def test_without_dummy(default_context: BuilderContext, orm: str):
    context = init_context(default_context, "postgresql", orm)
    context.add_dummy = False
    run_default_check(context)


@pytest.mark.parametrize(
    "api",
    [
        "rest",
        "graphql",
    ],
)
def test_redis(default_context: BuilderContext, api: str):
    default_context.enable_redis = True
    default_context.api_type = api
    run_default_check(default_context)


@pytest.mark.parametrize(
    "api",
    [
        "rest",
        "graphql",
    ],
)
def test_rmq(default_context: BuilderContext, api: str):
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


# @pytest.mark.parametrize("api", ["rest", "graphql"])
# def test_kafka(default_context: BuilderContext, api: str):
#     default_context.enable_kafka = True
#     default_context.api_type = api
#     run_default_check(default_context)
