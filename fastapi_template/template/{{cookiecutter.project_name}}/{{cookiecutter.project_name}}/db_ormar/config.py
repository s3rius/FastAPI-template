from databases import Database

from {{cookiecutter.project_name}}.settings import settings

database = Database(str(settings.db_url))
