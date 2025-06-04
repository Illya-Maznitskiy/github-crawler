from urllib.parse import urljoin

from utils.logger import logger


def extract_urls(soup):
    """
    Extract repository URLs from GitHub search results page soup.
    Returns a list of full repository URLs.
    """
    logger.info("Starting URL extraction for repositories")
    urls = []

    for h3 in soup.select("h3"):
        a_tag = h3.find("a")
        if a_tag:
            href = a_tag.get("href", "")
            # Repo URL pattern: /owner/repo
            if href.startswith("/") and href.count("/") == 2:
                full_url = urljoin("https://github.com", href)
                urls.append(full_url)

    logger.info(f"Extracted {len(urls)} repository URLs from the page.")
    return urls
