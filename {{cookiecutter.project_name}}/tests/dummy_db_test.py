import pytest
import sqlalchemy as sa
from sqlalchemy.engine import Connection
from starlette.testclient import TestClient

from src.models import DummyDBModel
from tests import TestSettings

test_data = [
    TestSettings(
        request_data=dict(
            dummy_id="b4439fc8-8fde-4079-ab2c-d61e46e22f25",
            json=dict(
                name="test dummy object",
                surname="Cesar"
            ),
        ),
    ),
]


@pytest.mark.parametrize("test_conf", test_data)
def test_delete_monitor(
        pg_conn: Connection, test_conf: TestSettings, app_fixture: TestClient
) -> None:
    with app_fixture as client:
        put_result = client.put(
            f"/dummy_db/{test_conf.request_data['dummy_id']}",
            json=test_conf.request_data["json"],
        )
        assert put_result.status_code == 200
        result = client.delete(f"/dummy_db/{test_conf.request_data['dummy_id']}")
        assert result.status_code == 200
        with pg_conn.begin():
            result = pg_conn.execute(sa.func.count(DummyDBModel.id)).first()
            assert result[0] == 0
