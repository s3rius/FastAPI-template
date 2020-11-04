import uuid
from typing import TypeVar, List, Optional, Any, Generic, Union, Dict

from elasticsearch import NotFoundError
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch
from loguru import logger

from src.services.elastic.client import elastic_client
from src.services.elastic.schema import ESReturnModel

SearchModel = TypeVar("SearchModel", covariant=True, bound=ESReturnModel)


class ElasticModelMixin(Generic[SearchModel]):
    __es_index_name: str = "default_index"
    __es_search_fields: List[str] = []
    __es_search_type: Optional[SearchModel] = None

    @classmethod
    async def elastic_add(
        cls, model_id: uuid.UUID, *, tags: Optional[str] = "", **kwargs: Any
    ) -> None:
        ret = await elastic_client.index(
            index=cls.__es_index_name,
            body={"tags": tags.split(",") if tags else [], **kwargs},
            id=str(model_id),
        )
        result = ret["result"]
        logger.debug(f"{result} '{cls.__name__}:{model_id}' in elastic")

    @classmethod
    async def elastic_filter(
        cls, *, query: str, offset: int, limit: int
    ) -> List[Union[SearchModel, Dict[str, Any]]]:
        elastic_query = Search()
        if query:
            elastic_query = elastic_query.query(
                MultiMatch(
                    type="phrase_prefix", query=query, fields=cls.__es_search_fields
                )
            )
        elastic_query = elastic_query[offset : offset + limit]
        search_res = await elastic_client.search(elastic_query.to_dict())
        hits = search_res.get("hits", {}).get("hits", [])
        results = []
        constructor = cls.__es_search_type or dict
        for hit in hits:
            logger.debug(hit)
            results.append(constructor(id=hit.get("_id"), **hit.get("_source", {})))
        return results

    @classmethod
    async def elastic_update(
        cls,
        model_id: uuid.UUID,
        **body: Any,
    ) -> None:
        tags = body.get("tags", None)
        if tags is not None:
            body["tags"] = tags.split(",") if tags else []
        logger.debug(f"Updating '{cls.__name__}:{model_id}' in ES")
        try:
            await elastic_client.update(
                index=cls.__es_index_name,
                id=str(model_id),
                body={"doc": body},
                refresh=True,
            )
        except NotFoundError:
            logger.debug(f"Can't update unknown {cls.__name__} in es")

    @classmethod
    async def elastic_delete(cls, model_id: uuid.UUID) -> None:
        try:
            await elastic_client.delete(index=cls.__es_index_name, id=str(model_id))
        except NotFoundError:
            logger.debug(f"'{cls.__name__}:{model_id}' was not found in ES")

    @classmethod
    async def elastic_create_index(cls) -> None:
        if not await elastic_client.indices.exists(cls.__es_index_name):
            logger.debug(f"Creating elastic index {cls.__es_index_name}")
            await elastic_client.indices.create(cls.__es_index_name)
