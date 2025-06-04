from urllib.parse import quote_plus
from bs4 import BeautifulSoup
import requests

from utils.logger import logger


def build_search_url(keywords, search_type):
    """
    Build a GitHub search URL using provided keywords and type.
    """
    base_url = "https://github.com/search"
    query = quote_plus(" ".join(keywords))  # handles spaces
    url = f"{base_url}?q={query}&type={search_type}"
    logger.info(f"Search URL built: {url}")
    return url


def check_proxy(
    proxy: str, test_url="http://httpbin.org/ip", timeout=3
) -> bool:
    """
    Test if the given proxy is working by sending a simple request.
    """
    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}",
    }
    try:
        response = requests.get(test_url, proxies=proxies, timeout=timeout)
        if response.status_code == 200:
            logger.info(f"Proxy is working: {proxy}")
            return True
        else:
            logger.warning(
                f"Proxy {proxy} responded with status {response.status_code}"
            )
            return False
    except requests.RequestException as e:
        logger.warning(f"Proxy failed: {proxy} ({e})")
        return False


def get_soup(url, proxy=None):
    """
    Fetch the HTML content from the URL using a working proxy (if any),
    and return a parsed BeautifulSoup object.
    """
    if proxy:
        if not check_proxy(proxy):
            logger.error(f"Proxy {proxy} is not working. Aborting.")
            raise Exception(f"Proxy {proxy} is not working")
    # if no proxy, stop the script
    else:
        logger.error("No proxy specified. Aborting.")
        raise Exception("No proxy specified.")

    try:
        response = requests.get(
            url,
            proxies={"http": proxy, "https": proxy} if proxy else None,
            timeout=10,
        )
        response.raise_for_status()
        logger.info(f"Successfully fetched URL: {url} with proxy: {proxy}")
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        logger.error(f"Request failed for {url} with proxy {proxy}: {e}")
        raise
