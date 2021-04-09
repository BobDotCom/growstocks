import growstocks
import pytest
import secrets


tests = [secrets.token_hex() for _ in range(1000)]


@pytest.fixture
def client():
    """Returns a client"""
    return growstocks.Client(12345, 'test')


@pytest.mark.parametrize("redirect_url", tests)
def test_conversions(client, redirect_url):
    assert client.auth.make_url(redirect_url)