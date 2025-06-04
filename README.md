# GitHub Crawler


## Description
A Python project that searches GitHub using keywords and shows the first page of results as links. It uses proxies to make requests and works without using the GitHub API.


## Technologies Used
- Python
- BeautifulSoup
- Logging
- Pytest


## Features
- Supports searching GitHub for Repositories, Issues, and Wikis using keywords
- Uses random proxy selection for each request to bypass rate limits
- Extracts and saves first-page search results as structured JSON output


## Setup
To install the project locally on your computer, execute the following commands in a terminal:
```bash
git clone https://github.com/Illya-Maznitskiy/github-crawler.git
cd github-crawler
python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)
pip install -r requirements.txt
```


## Creating an input.json File
Create an input.json file in the root project directory with the search keywords, proxy list, and search type. Below is a sample structure:
```json
{
  "keywords": ["openstack", "nova", "css"],
  "proxies": ["194.126.37.94:8080", "13.78.125.167:8080"],
  "type": "Repositories"
}
```


## Tests
You can run pytest and flake8 using the following commands:
```bash
pytest
flake8
```


## Run the project
Note: input.json is required before running. The results will be saved in the output.json file
Use the following commands to start the script:
```bash
python main.py
```


## Screenshots:
### Logging
![Logging](screenshots/logging.png)

### Output
![Output](screenshots/output.png)
