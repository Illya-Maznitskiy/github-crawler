import json

from utils.logger import logger


def get_data():
    """
    Load and validate input JSON data from 'input.json'.
    Returns a tuple of (keywords, proxies, type).
    """
    try:
        with open("input.json", "r") as f:
            data = f.read()
            dict_data = json.loads(data)
        logger.info("JSON data loaded successfully.")

        keywords = dict_data.get("keywords")
        proxies = dict_data.get("proxies")
        search_type = dict_data.get("type")

        # Basic validation
        if not isinstance(keywords, list):
            raise ValueError("keywords must be a list")
        if not isinstance(proxies, list):
            raise ValueError("proxies must be a list")
        if not isinstance(search_type, str):
            raise ValueError("type must be a string")

        allowed_types = ["repositories", "issues", "wikis"]

        if search_type.lower() not in allowed_types:
            raise ValueError("type must be one of {}".format(allowed_types))

        logger.info(
            f"Data validated: keywords={keywords}, proxies={proxies}, type={search_type}"
        )
        return keywords, proxies, search_type

    except Exception as e:
        logger.error(f"Error in get_data: {e}")
        raise
