from copy import copy

from worker.main import Worker


def test_init_worker():
    """Test: Init worker and check tasks list is not empty."""
    worker = Worker()
    assert len(worker.tasks) != 0


def test_task_price_movement_load_prices(task_price_movement):
    """Test: Load last prices from DB"""
    task_price_movement._load_last_prices()
    assert hasattr(task_price_movement, '_last_prices')


def test_task_price_movement_generate_movement(task_price_movement):
    """Test: Generate movement"""
    movement = task_price_movement._generate_movement()
    assert movement in (-1, 1)


def test_task_price_movement_generate_new_prices_info(task_price_movement):
    """Test: Generate new prices info"""
    task_price_movement._load_last_prices()
    last_prices = copy(task_price_movement._last_prices)
    new_prices_info = task_price_movement._generate_new_prices_info()
    for tool_id, new_price, *_ in new_prices_info:
        last_price = last_prices.get(tool_id)
        assert last_price is not None
        assert abs(last_price-new_price) == 1


def test_task_price_movement_update_price(task_price_movement):
    """Test: Update price."""
    task_price_movement._load_last_prices()
    last_prices = copy(task_price_movement._last_prices)
    new_prices = task_price_movement._last_prices
    task_price_movement._update_price()
    for tool_id, new_price in new_prices.items():
        last_price = last_prices.get(tool_id)
        assert last_price is not None
        assert abs(last_price-new_price) == 1
