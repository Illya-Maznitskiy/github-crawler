from bs4 import BeautifulSoup
from crawler.parse import extract_urls


def test_extract_urls_basic():
    """Test extracting valid repository URLs from sample HTML."""
    html = """
    <html>
        <body>
            <h3><a href="/owner1/repo1">Repo 1</a></h3>
            <h3><a href="/owner2/repo2">Repo 2</a></h3>
            <h3><a href="/not/a/repo/path">Not a repo</a></h3>
            <h3>No link here</h3>
        </body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    urls = extract_urls(soup)
    assert len(urls) == 2
    assert "https://github.com/owner1/repo1" in urls
    assert "https://github.com/owner2/repo2" in urls


def test_extract_urls_empty():
    """
    Test extraction returns empty list when no repository links are present.
    """
    html = "<html><body><h3>No links at all</h3></body></html>"
    soup = BeautifulSoup(html, "html.parser")
    urls = extract_urls(soup)
    assert urls == []


def test_extract_urls_ignore_invalid_href():
    """Test extraction ignores non-repo or incorrectly formatted URLs."""
    html = """
    <html>
        <body>
            <h3><a href="https://example.com/owner/repo">External Link</a></h3>
            <h3><a href="/owner/repo/subpath">Too deep</a></h3>
            <h3><a href="/owner/repo">Valid Repo</a></h3>
        </body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    urls = extract_urls(soup)
    assert urls == ["https://github.com/owner/repo"]
