from fastapi import FastAPI
from starlette.testclient import TestClient

from api import create_app


def test_create_app():
    """Test: Create app and check instance type is FastAPI."""
    app = create_app()
    assert isinstance(app, FastAPI)


def test_get_trade_tools(test_client: TestClient):
    """Test endpoint: Try to get trade tools"""
    res = test_client.get('/trade-tool/')
    assert res.status_code == 200


def test_get_price_history(test_client: TestClient):
    """Test endpoint: Try to get price history of special trade tool"""
    res = test_client.get('/trade-tool/1/history-price')
    assert res.status_code == 200


def test_get_price_history_not_found(test_client: TestClient):
    """Test endpoint: Failed get price history of unknown trade tool"""
    res = test_client.get('/trade-tool/999/history-price')
    assert res.status_code == 404
