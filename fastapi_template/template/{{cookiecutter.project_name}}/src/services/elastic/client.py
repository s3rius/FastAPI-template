from elasticsearch import AsyncElasticsearch
from src.settings import settings

elastic_client = AsyncElasticsearch(hosts=[settings.elastic_host])
