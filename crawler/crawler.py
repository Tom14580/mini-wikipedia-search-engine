from collections import deque
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import re
from utils.helpers import save_json
from pathlib import Path
from tqdm import tqdm

# get data directory path
SCRIPT_DIR = Path(__file__).parent.parent
DATA_DIR = SCRIPT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# setup session
session = requests.Session()
session.headers.update({
    "User-Agent": "MySearchEngine"
})

# takes a url and returns its info
def fetch_page(url: str) -> dict | None:
    # get the response from the url
    try:
        response = session.get(url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    # extract page title
    title = soup.title.string.strip() if soup.title else ""
    # gets all links on the page
    links = []
    for a in soup.find_all('a', href=True):
        new_url = urljoin(url, a['href'])
        links.append(new_url)
    
    return {
        "url": url,
        "title": title,
        "text": response.text,   # raw HTML — indexer will clean it
        "links": links
    }

# makes sure only english articles are added to queue
def is_article_url(url: str) -> bool:
    pattern = r'^https?://en\.wikipedia\.org/wiki/([^:#?]+)$'
    return bool(re.match(pattern, url))

# removes url fragments
def normalize_url(url: str) -> str:
    parsed = urlparse(url)
    clean = parsed._replace(fragment='', query='')
    return clean.geturl()

# makes sure the crawler stays on the same domain
def same_domain(url: str, base_domain: str = "en.wikipedia.org") -> bool:
    return urlparse(url).netloc == base_domain

# excludes certain paths that aren't relevant
def is_excluded_path(url: str) -> bool:
    excluded_prefixes = [
        "/wiki/Special:", "/wiki/Wikipedia:", "/wiki/Help:",
        "/wiki/Talk:", "/wiki/User:", "/wiki/File:", "/wiki/Template:"
    ]
    path = urlparse(url).path
    return any(path.startswith(p) for p in excluded_prefixes)

# crawls urls by calling fetch_page on them
def crawl(seed_urls: list[str], max_depth: int = 2, max_pages: int = 100) -> list[dict]:
    documents = []
    visited = set()
    queue = deque()

    # adds all seed urls to the queue to start with
    for url in seed_urls:
        if url not in visited:
            queue.append((url, 0))

    # progress bar to track crawling progress
    pbar = tqdm(total=max_pages, desc="Crawling")

    # loop until queue is empty or max_pages reached
    while queue and len(documents) < max_pages:
        # get the next url and its depth from the queue
        url, depth = queue.popleft()
        # if it has already been visited then skip it
        if url in visited or depth > max_depth:
            continue
        visited.add(url)

        # fetch the page and skip if it didn't return anything
        page_data = fetch_page(url)
        if page_data is None:
            continue
        
        # add the fetched data to documents
        documents.append(page_data)

        # update the progress bar
        pbar.update(1)

        # add each of the pages links to the queue
        for raw_link in page_data["links"]:
            full_url = normalize_url(urljoin(url, raw_link))
            if not same_domain(full_url):        # stay on English Wikipedia
                continue
            if is_excluded_path(full_url):       # skip non‑article pages
                continue
            if not is_article_url(full_url):     # only main article pages
                continue
            if full_url not in visited:
                queue.append((full_url, depth + 1))
    
    pbar.close()
    if documents:
        save_json(documents, str(DATA_DIR / "documents.json"))
    return documents