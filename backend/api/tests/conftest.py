import pytest
from starlette.testclient import TestClient

from api.app import create_app
from utils.db.models import migrate

app = create_app()
migrate()


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(app)
