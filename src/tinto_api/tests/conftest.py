"""
Pytest configuration and shared fixtures for all tests.
"""
import pytest
import os
from fastapi.testclient import TestClient
from tinto.main import tinto

os.environ["TESTING"] = "true"


@pytest.fixture(scope="session")
def client():
    return TestClient(tinto)


@pytest.fixture
def test_user_data():
    return {
        "full_name": "Test User",
        "cpf": "123.456.789-00",
        "birth_date": "1990-01-01",
        "gender": "M",
        "phone_number": "11999999999",
        "email": "testuser@example.com",
        "password": "TestPassword123!"
    }


@pytest.fixture
def test_admin_data():
    return {
        "full_name": "Test Admin",
        "cpf": "987.654.321-00",
        "birth_date": "1985-05-15",
        "gender": "M",
        "phone_number": "11988888888",
        "email": "testadmin@example.com",
        "password": "AdminPassword123!"
    }


@pytest.fixture
def test_flight_data():
    return {
        "airline_id": 1,
        "departure_airport": "GIG",
        "arrival_airport": "SDU",
        "departure_time": "2025-12-01T10:00:00",
        "arrival_time": "2025-12-01T11:30:00",
        "base_price": 500.00,
        "available_seats": 100
    }


@pytest.fixture
def test_airline_data():
    """Provide sample airline data."""
    return {
        "name": "Test Airlines",
        "iata_code": "TST",
        "icao_code": "TEST",
        "country": "Brazil"
    }


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
