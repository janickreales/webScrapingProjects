import requests
import threading
import concurrent.futures
from bs4 import BeautifulSoup

thread_local = threading.local()

def extract_soup(page):
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'}
    # page = requests.get(url, headers=headers, params=params)
    soup = BeautifulSoup(page.text, 'html.parser')

    return soup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'}

def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def download_site(url):
    session = get_session()
    with session.get(url,headers=headers) as response:
        # print(f"Read {len(response.content)} from {url}")
        print(len(response.text))


def download_all_sites(sites):
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(download_site, sites)