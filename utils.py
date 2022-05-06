import requests
import re
from dataclasses import dataclass
from typing import List, Tuple, Union
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
headers = {'User-Agent': 'Mozilla/5.0'}


def get_soup(url: str) -> Tuple[int, BeautifulSoup]:
    """handles getting a soup from a given url"""
    page = http.get(url, headers=headers)
    return page.status_code, BeautifulSoup(page.content, 'html.parser')


def login() -> None:
    """Logs you into an ao3 account"""
    username, password = get_credentials()
    if username == "":
        print("Login failed: No credentials provided. Skipping login process...")
        return
    login_status, login_soup = get_soup("https://archiveofourown.org/users/login")
    if login_status != 200:
        print(f"Login failed: Could not fetch login page. Received status code {login_status}. Skipping login process...")
        return
    authenticity_tag = login_soup.select("meta[name=csrf-token]")[0]
    authenticity_token = authenticity_tag.get("content")
    payload = {
        "authenticity_token": authenticity_token,
        "user[login]": username,
        "user[password]": password,
        "user[remember_me]": "0",
        "commit":  "Log+in"
    }
    response = http.post("https://archiveofourown.org/users/login", data=payload, headers=headers)
    if response.status_code != 200:
        print("Login failed: Login request was unsuccessful. Are you sure you provided the correct username and password? Skipping login process...")
        return
    print("Login success!")


def get_credentials() -> Tuple[str, str]:
    with open("credentials.txt", "r") as f:
        contents = f.read()
        if len(contents) <= 1:
            return "", ""
        credentials_list = contents.split("\n")
        return credentials_list[0], credentials_list[1]


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
