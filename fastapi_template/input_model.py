import enum
from typing import Optional

from pydantic import BaseModel


@enum.unique
class DatabaseType(enum.Enum):
    none = "none"
    sqlite = "sqlite"
    mysql = "mysql"
    postgresql = "postgresql"


@enum.unique
class CIType(enum.Enum):
    none = "none"
    gitlab_ci = "gitlab"
    github = "github"

@enum.unique
class ORM(enum.Enum):
    none = "none"
    ormar = "ormar"
    sqlalchemy = "sqlalchemy"
    tortoise = "tortoise"


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
        image="postgres:13.4-buster",
        async_driver="postgresql+asyncpg",
        driver_short="postgres",
        driver="postgresql",
        port=5432,
    ),
    DatabaseType.mysql: Database(
        name=DatabaseType.mysql.value,
        image="bitnami/mysql:8.0.26",
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


class BuilderContext(BaseModel):
    """Options for project generation."""

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
    force: bool = False

    class Config:
        orm_mode = True
