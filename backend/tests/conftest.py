import pytest
from starlette.testclient import TestClient

from api.app import create_app
from utils.db.models import migrate
from worker.tasks import PriceMovement

app = create_app()
migrate()


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def task_price_movement() -> PriceMovement:
    return PriceMovement()

