import uuid
from typing import Optional

from sqlalchemy import Column, String, sql
{% if cookiecutter.add_elastic_search == "True" -%}
from src.services.elastic import ElasticModelMixin
from src.services.elastic.schema import ESReturnModel
{% endif %}
from src.services.db import Base

{% if cookiecutter.add_elastic_search == "True" -%}
class DummyElasticFilter(ESReturnModel):
    name: str
    surname: str
{% endif %}

class DummyDBModel(Base{% if cookiecutter.add_elastic_search == "True" -%}, ElasticModelMixin[DummyElasticFilter]{% endif %}):
    name = Column(String, nullable=False, index=True)
    surname = Column(String, nullable=False, index=True)
    {% if cookiecutter.add_elastic_search == "True" -%}
    tags = Column(String, nullable=False, default="")

    __es_index_name = "dummy_elastic_index"
    __es_search_fields = ["name", "surname"]
    __es_search_type = DummyElasticFilter
    {% endif %}

    @classmethod
    def create(
            cls,
            *,
            name: str,
            surname: str,
            {% if cookiecutter.add_elastic_search == "True" -%}tags: str = "",{% endif %}
    ) -> sql.Insert:
        return cls.insert_query(
            name=name,
            surname=surname,
            {% if cookiecutter.add_elastic_search == "True" -%}tags=tags,{% endif %}
        )

    @classmethod
    def delete(cls, dummy_id: uuid.UUID) -> sql.Delete:
        return cls.delete_query().where(cls.id == dummy_id)

    @classmethod
    def update(cls,
               dummy_id: uuid.UUID,
               *,
               name: Optional[str] = None,
               surname: Optional[str] = None,
               {% if cookiecutter.add_elastic_search == "True" -%}tags: Optional[str] = None,{% endif %}
               ) -> sql.Update:
        new_values = {}
        if name:
            new_values[cls.name] = name
        if surname:
            new_values[cls.surname] = surname
        if tags is not None:
            new_values[cls.tags] = tags
        return cls.update_query().where(cls.id == dummy_id).values(new_values)

    @classmethod
    def filter(cls, *,
               dummy_id: Optional[uuid.UUID] = None,
               name: Optional[str] = None,
               surname: Optional[str] = None
               ) -> sql.Select:
        query = cls.select_query()
        if dummy_id:
            query = query.where(cls.id == dummy_id)
        if name:
            query = query.where(cls.name == name)
        if surname:
            query = query.where(cls.surname == surname)
        return query
