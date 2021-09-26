from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette import status


def test_health(client: TestClient, fastapi_app: FastAPI) -> None:
    """
    Checks the health endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    """
    url = fastapi_app.url_path_for('health_check')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
