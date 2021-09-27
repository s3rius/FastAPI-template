import uuid

from fastapi.testclient import TestClient
from fastapi import FastAPI
from starlette import status

def test_echo(fastapi_app: FastAPI, client: TestClient) -> None:
    """
    Tests that echo route works.

    :param fastapi_app: current application.
    :param client: clien for the app.
    """
    url = fastapi_app.url_path_for('send_echo_message')
    message = uuid.uuid4().hex
    response = client.post(url, json={
        "message": message
    })
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['message'] == message

