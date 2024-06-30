import sqlalchemy as sa
from databases import Database
from ormar import OrmarConfig
from {{cookiecutter.project_name}}.settings import settings

meta = sa.MetaData()
database = Database(str(settings.db_url))

ormar_config = OrmarConfig(metadata=meta, database=database)

