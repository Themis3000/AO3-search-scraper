import requests
import re
from dataclasses import dataclass
from typing import List, Tuple
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

retry_strategy = Retry(
    total=10,
    backoff_factor=120,
    status_forcelist=[429, 500, 502, 503, 504],
    method_whitelist=["HEAD", "GET", "OPTIONS"]
)

adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)


def get_soup(url: str) -> Tuple[int, BeautifulSoup]:
    """handles getting a soup from a given url"""
    page = http.get(url)
    return page.status_code, BeautifulSoup(page.content, 'html.parser')


@dataclass
class Work:
    title: str
    link: str
    author: str = "Anonymous"
    id: int = None
    dl_link: str = None

    def __post_init__(self):
        self.id = re.findall("^[^\d]*(\d+)", self.link)[0]
        self.dl_link = f"https://archiveofourown.org/downloads/{self.id}/work.pdf"


@dataclass
class Page:
    works: List[Work]
    next_url: str = None


def get_valid_filename(s: str) -> str:
    s = str(s).strip()
    return re.sub(r'(?u)[^-\w.\[\]() ]', '', s)
