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


class Database(BaseModel):
    name: str
    image: Optional[str]
    driver: Optional[str]
    port: Optional[int]

DB_INFO = {
    DatabaseType.none: Database(
        name="none",
        image=None,
        driver=None,
        port=None,
    ),
    DatabaseType.postgresql: Database(
        name=DatabaseType.postgresql.value,
        image="postgres:13.4-buster",
        driver="postgresql+asyncpg",
        port=5432,
    ),
    DatabaseType.mysql: Database(
        name=DatabaseType.mysql.value,
        image="bitnami/mysql:8.0.26",
        driver="mysql+aiomysql",
        port=3306,
    ),
    DatabaseType.sqlite: Database(
        name=DatabaseType.sqlite.value, image=None, driver="sqlite+aiosqlite", port=None
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
    enable_alembic: Optional[bool]
    enable_kube: Optional[bool]
    enable_routers: Optional[bool]
    add_dummy: Optional[bool] = False
    self_hosted_swagger: Optional[bool]
    force: bool = False

    class Config:
        orm_mode = True
