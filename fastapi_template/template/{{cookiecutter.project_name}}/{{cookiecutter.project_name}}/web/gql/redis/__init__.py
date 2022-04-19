"""Redis API."""
from {{cookiecutter.project_name}}.web.gql.redis.mutation import Mutation
from {{cookiecutter.project_name}}.web.gql.redis.query import Query

__all__ = ["Query", "Mutation"]
