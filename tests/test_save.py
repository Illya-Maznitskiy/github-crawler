import json
import os
import tempfile
from crawler.save import save_results_to_json


def test_save_results_to_json():
    """Test saving URL results to a JSON file and verify file contents."""
    results = [
        "https://github.com/owner/repo1",
        "https://github.com/owner/repo2",
    ]

    # Create a temporary file to save JSON data
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp_file:
        filename = tmp_file.name

    # Use try-finally to ensure a temporary file is deleted after test
    try:
        save_results_to_json(results, filename)

        # Read back the file and verify its contents
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert isinstance(data, list)
        assert all("url" in item for item in data)
        assert [item["url"] for item in data] == results
    finally:
        os.remove(filename)
