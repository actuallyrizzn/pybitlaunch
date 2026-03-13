"""Test Client and service wiring."""
import pytest


def test_client_has_all_services(token):
    """Client exposes Account, SSHKeys, Transactions, Servers, CreateOptions, Domains."""
    import pybitlaunch
    client = pybitlaunch.Client(token)
    assert client.Account is not None
    assert client.SSHKeys is not None
    assert client.Transactions is not None
    assert client.Servers is not None
    assert client.CreateOptions is not None
    assert client.Domains is not None


def test_client_domains_is_domains_service(token):
    """Domains attribute is DomainsService instance."""
    import pybitlaunch
    from pybitlaunch.Domains import DomainsService
    client = pybitlaunch.Client(token)
    assert isinstance(client.Domains, DomainsService)


def test_import_exports():
    """Public API exports Record and DomainsService."""
    import pybitlaunch
    assert hasattr(pybitlaunch, "Record")
    assert hasattr(pybitlaunch, "DomainsService")
    assert hasattr(pybitlaunch, "Client")
