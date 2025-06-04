import pytest
from unittest.mock import patch, Mock

import requests
from bs4 import BeautifulSoup
from crawler.fetcher import build_search_url, check_proxy, get_soup


def test_build_search_url():
    """
    Test that build_search_url correctly constructs the GitHub search URL.
    """
    keywords = ["python", "web scraping"]
    search_type = "repositories"
    url = build_search_url(keywords, search_type)
    assert "python+web+scraping" in url
    assert "type=repositories" in url


@patch("crawler.fetcher.requests.get")
def test_test_proxy_success(mock_get):
    """Test test_proxy returns True when the proxy responds with status 200."""
    # Mock successful response
    mock_resp = Mock()
    mock_resp.status_code = 200
    mock_get.return_value = mock_resp

    assert check_proxy("1.2.3.4:8080") is True
    mock_get.assert_called_once()


@patch("crawler.fetcher.requests.get")
def test_test_proxy_failure_status(mock_get):
    """
    Test test_proxy returns False when proxy responds with non-200 status.
    """
    # Mock failure response status code != 200
    mock_resp = Mock()
    mock_resp.status_code = 403
    mock_get.return_value = mock_resp

    assert check_proxy("1.2.3.4:8080") is False


@patch("crawler.fetcher.requests.get")
def test_test_proxy_exception(mock_get):
    """Test test_proxy returns False when requests.get raises an exception."""
    # Use a requests.RequestException subclass to simulate connection error
    mock_get.side_effect = requests.exceptions.RequestException(
        "Connection error"
    )

    assert check_proxy("1.2.3.4:8080") is False


@patch("crawler.fetcher.check_proxy")
@patch("crawler.fetcher.requests.get")
def test_get_soup_with_working_proxy(mock_get, mock_check_proxy):
    """Test get_soup returns BeautifulSoup object when the proxy is working."""
    mock_check_proxy.return_value = True
    html = "<html><head><title>Test</title></head><body></body></html>"
    mock_resp = Mock()
    mock_resp.status_code = 200
    mock_resp.text = html
    mock_get.return_value = mock_resp

    # Verify get_soup returns parsed HTML and uses proxy
    soup = get_soup("http://example.com", proxy="1.2.3.4:8080")
    assert isinstance(soup, BeautifulSoup)
    assert soup.title.string == "Test"
    mock_check_proxy.assert_called_once_with("1.2.3.4:8080")
    mock_get.assert_called_once()


@patch("crawler.fetcher.check_proxy")
def test_get_soup_with_failing_proxy(mock_check_proxy):
    """Raise exception if proxy test fails in get_soup."""
    mock_check_proxy.return_value = False
    with pytest.raises(Exception, match="Proxy 1.2.3.4:8080 is not working"):
        get_soup("http://example.com", proxy="1.2.3.4:8080")


def test_get_soup_no_proxy():
    """Raise exception when no proxy is given to get_soup."""
    with pytest.raises(Exception, match="No proxy specified"):
        get_soup("http://example.com", proxy=None)
