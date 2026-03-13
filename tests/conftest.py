"""Pytest fixtures and shared mocks."""
import pytest


@pytest.fixture
def token():
    return "test-token"


@pytest.fixture
def domain():
    return "example.com"


@pytest.fixture
def sample_record_list():
    """Sample API response for List records."""
    return [
        {"id": "rec-1", "hostname": "@", "type": "A", "value": "1.2.3.4", "ttl": 3600},
        {"id": "rec-2", "hostname": "www", "type": "CNAME", "value": "example.com.", "ttl": 3600},
    ]


@pytest.fixture
def sample_record_obj():
    """Single record as returned by API."""
    return {"id": "rec-1", "uid": "uid-1", "hostname": "@", "type": "A", "value": "1.2.3.4", "ttl": 3600}
