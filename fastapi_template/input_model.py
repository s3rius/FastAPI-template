import enum
from typing import Optional

from pydantic import BaseModel


@enum.unique
class APIType(enum.Enum):
    rest = "rest"
    graphql = "graphql"

@enum.unique
class DatabaseType(enum.Enum):
    none = "none"
    sqlite = "sqlite"
    mysql = "mysql"
    postgresql = "postgresql"


@enum.unique
class CIType(enum.Enum):
    none = "none"
    gitlab_ci = "gitlab_ci"
    github = "github"

@enum.unique
class ORM(enum.Enum):
    none = "none"
    ormar = "ormar"
    sqlalchemy = "sqlalchemy"
    tortoise = "tortoise"
    psycopg = "psycopg"
    piccolo = "piccolo"


class Database(BaseModel):
    name: str
    image: Optional[str]
    driver: Optional[str]
    async_driver: Optional[str]
    driver_short: Optional[str]
    port: Optional[int]


DB_INFO = {
    DatabaseType.none: Database(
        name="none",
        image=None,
        driver=None,
        async_driver=None,
        port=None,
    ),
    DatabaseType.postgresql: Database(
        name=DatabaseType.postgresql.value,
        image="postgres:13.6-bullseye",
        async_driver="postgresql+asyncpg",
        driver_short="postgres",
        driver="postgresql",
        port=5432,
    ),
    DatabaseType.mysql: Database(
        name=DatabaseType.mysql.value,
        image="bitnami/mysql:8.0.28",
        async_driver="mysql+aiomysql",
        driver_short="mysql",
        driver="mysql",
        port=3306,
    ),
    DatabaseType.sqlite: Database(
        name=DatabaseType.sqlite.value,
        image=None,
        async_driver="sqlite+aiosqlite",
        driver_short="sqlite",
        driver="sqlite",
        port=None,
    ),
}

SUPPORTED_ORMS = {
    DatabaseType.postgresql: [
        ORM.ormar,
        ORM.psycopg,
        ORM.tortoise,
        ORM.sqlalchemy,
        ORM.piccolo,
    ],
    DatabaseType.sqlite: [
        ORM.ormar,
        ORM.tortoise,
        ORM.sqlalchemy,
        ORM.piccolo,
    ],
    DatabaseType.mysql: [
        ORM.ormar,
        ORM.tortoise,
        ORM.sqlalchemy,
    ]
}

ORMS_WITHOUT_MIGRATIONS = [
    ORM.psycopg,
]

class BuilderContext(BaseModel):
    """Options for project generation."""
    api_type: Optional[APIType]
    project_name: Optional[str]
    kube_name: Optional[str]
    project_description: Optional[str]
    db: Optional[DatabaseType]
    db_info: Optional[Database]
    enable_redis: Optional[bool]
    ci_type: Optional[CIType]
    orm: Optional[ORM]
    enable_migrations: Optional[bool]
    enable_kube: Optional[bool]
    enable_routers: Optional[bool]
    add_dummy: Optional[bool] = False
    self_hosted_swagger: Optional[bool]
    enable_rmq: Optional[bool]
    force: bool = False
    quite: bool = False

    class Config:
        orm_mode = True
