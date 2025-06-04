import json
import os

import pytest

from crawler.input import get_data


def write_input(tmp_path, data):
    """Write data as JSON to 'input.json' in the given path."""
    json_file = tmp_path / "input.json"
    json_file.write_text(json.dumps(data))
    return json_file


def test_get_data_valid(tmp_path):
    """
    Test get_data() correctly loads and validates input JSON data.
    """
    input_data = {
        "keywords": ["python", "api"],
        "proxies": ["127.0.0.1:8080"],
        "type": "repositories",
    }
    write_input(tmp_path, input_data)

    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        keywords, proxies, search_type = get_data()
    finally:
        os.chdir(old_cwd)

    assert keywords == ["python", "api"]
    assert proxies == ["127.0.0.1:8080"]
    assert search_type == "repositories"


def test_validation_keywords_not_list(tmp_path):
    """Raise ValueError if keywords is not a list."""
    data = {
        "keywords": "not-a-list",
        "proxies": ["127.0.0.1:8080"],
        "type": "repositories",
    }
    write_input(tmp_path, data)
    os.chdir(tmp_path)
    with pytest.raises(ValueError, match="keywords must be a list"):
        get_data()


def test_validation_proxies_not_list(tmp_path):
    """Raise ValueError if proxies is not a list."""
    data = {
        "keywords": ["python"],
        "proxies": "not-a-list",
        "type": "repositories",
    }
    write_input(tmp_path, data)
    os.chdir(tmp_path)
    with pytest.raises(ValueError, match="proxies must be a list"):
        get_data()


def test_validation_type_invalid(tmp_path):
    """Raise ValueError if type is not one of the allowed values."""
    data = {
        "keywords": ["python"],
        "proxies": ["127.0.0.1:8080"],
        "type": "invalid-type",
    }
    write_input(tmp_path, data)
    os.chdir(tmp_path)
    with pytest.raises(ValueError, match="type must be one of"):
        get_data()
