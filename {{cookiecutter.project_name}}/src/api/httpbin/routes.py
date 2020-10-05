from fastapi import APIRouter

from src.services.httpbin.client import http_bin_service
from src.services.httpbin.schema import DummyHttpBinObj, HTTPBinResponse

router = APIRouter()
URL_PREFIX = "/http_bin"


@router.put("/", response_model=HTTPBinResponse)
async def create_dummy_obj(dummy_obj: DummyHttpBinObj) -> HTTPBinResponse:
    return await http_bin_service.put_req(dummy_obj)


@router.delete("/{obj_id}", response_model=HTTPBinResponse)
async def delete_dummy_obj(obj_id: str) -> HTTPBinResponse:
    return await http_bin_service.delete_req(obj_id)
