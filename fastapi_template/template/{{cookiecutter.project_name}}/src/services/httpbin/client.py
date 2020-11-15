from httpx import AsyncClient, Response
from loguru import logger

from src.exceptions import ServiceError
from src.services.httpbin.schema import DummyHttpBinObj, HTTPBinResponse
from src.settings import settings


class HttpBinService:
    def __init__(self, http_bin_host: str) -> None:
        self.host = http_bin_host

    @property
    def client(self) -> AsyncClient:
        """
        Generate a client with base_url
        :return: async http client
        """
        return AsyncClient(
            base_url=self.host
        )

    @classmethod
    def catch_response(cls, response: Response, action: str, *codes: int) -> None:
        logger.debug("Response got")
        logger.debug(response.url)
        logger.debug(response.status_code)
        logger.debug(response.headers)
        logger.debug(response.text)
        if response.status_code not in codes:
            raise ServiceError(action, response)

    async def put_req(self, dummy_obj: DummyHttpBinObj) -> HTTPBinResponse:
        """
        Create dummy object in HTTPBin API.
        :param dummy_obj: target to create
        :return: None if success, raise an error if status code is not 201
        """
        async with self.client as http:
            response = await http.put("/put", json=dummy_obj.dict())
            self.catch_response(response, "Create dummy object", 200)
        return HTTPBinResponse(**response.json())

    async def delete_req(self, dummy_id: str) -> HTTPBinResponse:
        """
        Delete dummy_obj from HTTPBin API.
        :param dummy_id: target to delete
        :return: None if success, raise an error if status code is not 200
        """
        async with self.client as http:
            response = await http.delete("/delete", params={
                "dummy_id": dummy_id
            })
            self.catch_response(response, "delete bucket", 200)
        return HTTPBinResponse(**response.json())


http_bin_service = HttpBinService(
    settings.httpbin_host
)
