import concurrent.futures
import os.path
from utils import Page, Work, get_soup, get_valid_filename, http, login


with open("page.txt", "r") as f:
    starting_link = f.read()


def analyze_page_url(url: str) -> Page:
    """analyzes the url of a page and returns a Page object"""
    status, page_soup = get_soup(url)
    if status != 200:
        print(f"failed to fetch page {url}")
    headings = page_soup.select("div.header.module > h4.heading")

    works = []
    for heading in headings:
        a_heads = heading.select("a")
        title = a_heads[0].string
        link = a_heads[0].get("href")
        author = "Anonymous" if len(a_heads) == 1 else a_heads[1].string
        work = Work(title, link, author)
        works.append(work)

    next_button_search = page_soup.select("li.next > a")
    if len(next_button_search) == 0:
        return Page(works)
    next_button = next_button_search[0]
    next_url = "https://archiveofourown.org" + next_button.get("href")
    return Page(works, next_url)


def work_dl(work: Work, dir_path="./downloads") -> None:
    """Downloads a work"""
    filename = get_valid_filename(f"{work.title} - {work.author} ({work.id})")
    filepath = f"{dir_path}/{filename}.pdf"
    if os.path.isfile(filename):
        print(f"skipping {work.title} by {work.author} - already downloaded")
        return
    response = http.get(work.dl_link)
    if response.status_code != 200:
        print(f"failed to fetch {filename}.pdf")
    open(filepath, "wb").write(response.content)


login()
page_url = starting_link
page_number = 1
while True:
    page = analyze_page_url(page_url)

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(work_dl, page.works)
    print(f"scraped page {page_number}")

    if page.next_url is None:
        print(f"halted on page {page_number}")
        break

    page_url = page.next_url
    with open("page.txt", "w+") as f:
        f.write(page_url)
    page_number += 1
