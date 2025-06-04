import random

from crawler.fetcher import build_search_url, get_soup
from crawler.input import get_data
from crawler.parse import extract_urls
from crawler.save import save_results_to_json


def main():
    """
    Run the GitHub crawler: load input data, build search URL,
    select a proxy, fetch and parse the page, then print the title.
    """
    keywords, proxies, search_type = get_data()
    url = build_search_url(keywords, search_type)
    proxy = random.choice(proxies)
    soup = get_soup(url, proxy)
    urls = extract_urls(soup)
    save_results_to_json(urls, filename="output.json")


if __name__ == "__main__":
    main()
