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


class BuilderContext(BaseModel):
    """Options for project generation."""

    project_name: Optional[str]
    project_description: Optional[str]
    db: Optional[DatabaseType]
    db_info: Optional[Database]
    enable_redis: Optional[bool]
    ci_type: Optional[CIType]
    enable_alembic: Optional[bool]
    enable_kube: Optional[bool]
    force: bool = False

    class Config:
        orm_mode = True
