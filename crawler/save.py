import json

from utils.logger import logger


def save_results_to_json(results, filename="output.json"):
    """
    Save list of URLs to a JSON file.
    """
    data = [{"url": url} for url in results]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logger.info(f"Saved {len(results)} results {results} to {filename}")
