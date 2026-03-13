"""Smoke tests for Account, Servers, SSHKeys, Transactions, CreateOptions (no real API)."""
import pytest
from unittest.mock import patch

import pybitlaunch


def test_account_service_show_mock(token):
    """Account.Show exists and can be mocked."""
    with patch.object(pybitlaunch.AccountService, "getData") as mock_get:
        mock_get.return_value = {"email": "test@example.com"}
        client = pybitlaunch.Client(token)
        data = client.Account.Show()
        assert data["email"] == "test@example.com"
        mock_get.assert_called_once()


def test_servers_list_mock(token):
    """Servers.List exists and can be mocked."""
    with patch.object(pybitlaunch.ServerService, "getData") as mock_get:
        mock_get.return_value = []
        client = pybitlaunch.Client(token)
        data, err = client.Servers.List()
        assert err is None
        assert data == []
        mock_get.assert_called_once()


def test_create_options_show_mock(token):
    """CreateOptions.Show exists and can be mocked."""
    with patch.object(pybitlaunch.CreateOptionsService, "getData") as mock_get:
        mock_get.return_value = {"image": [], "region": []}
        client = pybitlaunch.Client(token)
        data, err = client.CreateOptions.Show(4)
        assert err is None
        mock_get.assert_called_once()


def test_client_requires_token_for_api_calls():
    """Client with empty token raises TokenError on API call."""
    from pybitlaunch.BaseAPI import TokenError
    client = pybitlaunch.Client("")
    with pytest.raises(TokenError):
        client.Account.Show()
