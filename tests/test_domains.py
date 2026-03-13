"""Test Domains service and Record (mocked API)."""
import pytest
from unittest.mock import patch, MagicMock

import pybitlaunch
from pybitlaunch import Record, DomainsService


class TestRecord:
    """Test Record model."""

    def test_record_attributes(self):
        r = Record(hostname="@", type="A", value="1.2.3.4", ttl=3600)
        assert r.hostname == "@"
        assert r.type == "A"
        assert r.value == "1.2.3.4"
        assert r.ttl == 3600
        assert r.id is None
        assert r.uid is None

    def test_record_optional_fields(self):
        r = Record(hostname="www", type="CNAME", value="example.com.", priority=10, weight=5, port=443)
        assert r.priority == 10
        assert r.weight == 5
        assert r.port == 443
        assert r.caaflag is None
        assert r.caatype is None


class TestDomainsServiceList:
    """Test Domains.List."""

    def test_list_empty_domain_returns_error(self, token):
        svc = DomainsService(token)
        data, err = svc.List("")
        assert data is None
        assert "domain" in err.lower()

    def test_list_none_domain_returns_error(self, token):
        svc = DomainsService(token)
        data, err = svc.List(None)
        assert data is None
        assert err is not None

    @patch.object(DomainsService, "getData")
    def test_list_success_returns_data(self, mock_get, token, domain, sample_record_list):
        mock_get.return_value = sample_record_list
        svc = DomainsService(token)
        data, err = svc.List(domain)
        assert err is None
        assert data == sample_record_list
        mock_get.assert_called_once()
        call_url = mock_get.call_args[0][0]
        assert "domains" in call_url and domain in call_url and "records" in call_url

    @patch.object(DomainsService, "getData")
    def test_list_api_message_returns_error(self, mock_get, token, domain):
        mock_get.return_value = {"message": "Domain not found"}
        svc = DomainsService(token)
        data, err = svc.List(domain)
        assert data is None
        assert err == "Domain not found"


class TestDomainsServiceShow:
    """Test Domains.Show."""

    @patch.object(DomainsService, "getData")
    def test_show_success(self, mock_get, token, domain, sample_record_obj):
        mock_get.return_value = sample_record_obj
        svc = DomainsService(token)
        data, err = svc.Show(domain, "rec-1")
        assert err is None
        assert data["id"] == "rec-1"
        assert "domains" in mock_get.call_args[0][0] and "records" in mock_get.call_args[0][0]

    def test_show_missing_record_id_returns_error(self, token, domain):
        svc = DomainsService(token)
        data, err = svc.Show(domain, None)
        assert data is None
        assert "record" in err.lower() or "id" in err.lower()


class TestDomainsServiceCreate:
    """Test Domains.Create."""

    def test_create_empty_domain_returns_error(self, token):
        svc = DomainsService(token)
        r = Record(hostname="@", type="A", value="1.2.3.4")
        data, err = svc.Create("", r)
        assert data is None
        assert "domain" in err.lower()

    def test_create_none_record_returns_error(self, token, domain):
        svc = DomainsService(token)
        data, err = svc.Create(domain, None)
        assert data is None
        assert "record" in err.lower()

    def test_create_missing_value_returns_error(self, token, domain):
        svc = DomainsService(token)
        r = Record(hostname="@", type="A", value=None)
        data, err = svc.Create(domain, r)
        assert data is None
        assert "value" in err.lower()

    @patch.object(DomainsService, "getData")
    def test_create_success(self, mock_get, token, domain, sample_record_obj):
        mock_get.return_value = sample_record_obj
        svc = DomainsService(token)
        r = Record(hostname="@", type="A", value="1.2.3.4", ttl=3600)
        data, err = svc.Create(domain, r)
        assert err is None
        assert data["id"] == "rec-1"
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert call_args[1]["type"] == pybitlaunch.POST
        params = call_args[1]["params"]
        assert params.get("hostname") == "@" and params.get("type") == "A" and params.get("value") == "1.2.3.4"


class TestDomainsServiceUpdate:
    """Test Domains.Update."""

    def test_update_missing_record_id_returns_error(self, token, domain):
        svc = DomainsService(token)
        r = Record(hostname="@", type="A", value="2.3.4.5")
        data, err = svc.Update(domain, None, r)
        assert data is None
        assert err is not None

    @patch.object(DomainsService, "getData")
    def test_update_success(self, mock_get, token, domain, sample_record_obj):
        mock_get.return_value = {**sample_record_obj, "value": "2.3.4.5"}
        svc = DomainsService(token)
        r = Record(value="2.3.4.5")
        data, err = svc.Update(domain, "rec-1", r)
        assert err is None
        assert data["value"] == "2.3.4.5"
        call_args = mock_get.call_args
        assert call_args[1]["type"] == pybitlaunch.PUT
        assert "rec-1" in call_args[0][0]


class TestDomainsServiceDelete:
    """Test Domains.Delete."""

    def test_delete_empty_domain_returns_error(self, token):
        svc = DomainsService(token)
        err = svc.Delete("", "rec-1")
        assert err is not None
        assert "domain" in err.lower()

    def test_delete_missing_record_id_returns_error(self, token, domain):
        svc = DomainsService(token)
        err = svc.Delete(domain, None)
        assert err is not None

    @patch.object(DomainsService, "getData")
    def test_delete_success_returns_none(self, mock_get, token, domain):
        mock_get.return_value = None
        svc = DomainsService(token)
        err = svc.Delete(domain, "rec-1")
        assert err is None
        call_args = mock_get.call_args
        assert call_args[1]["type"] == pybitlaunch.DELETE

    @patch.object(DomainsService, "getData")
    def test_delete_api_message_returns_message(self, mock_get, token, domain):
        mock_get.return_value = {"message": "Forbidden"}
        svc = DomainsService(token)
        err = svc.Delete(domain, "rec-1")
        assert err == "Forbidden"
