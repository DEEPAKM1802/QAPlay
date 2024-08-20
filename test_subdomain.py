from Contracts.test_contract import TestExecutionAsync
from Utilities.Data_Structures import TestResult, TestStatus, ComparisonResult
import asyncio
import nest_asyncio
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from queue import Queue
import threading

import asyncio
from queue import Queue
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from playwright.async_api import Page
import threading

# Apply the nested event loop patch
# nest_asyncio.apply()


import asyncio
from queue import Queue
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from playwright.async_api import Page
import threading
nest_asyncio.apply()

class WebCrawlerTest(TestExecutionAsync):

    def run_test(self) -> TestResult:
        crawler = WebCrawler(self.context, self.context.url)
        internal_pages, external_pages = crawler.main()
        self.site.internal_pages.extend(internal_pages)
        self.site.external_pages.extend(external_pages)
        print("Internal Pages:", len(internal_pages), len(set(internal_pages)))
        print("Subdomains:", len(external_pages))
        return TestResult(
            Name="Web Crawler Test",
            Status=TestStatus.PASS,
            Description="Discovered additional internal pages.",
            Actual_Result=internal_pages
        )

    def run_comparison(self, results) -> ComparisonResult:
        return ComparisonResult(
            Name="Web Crawler Test",
            Status=TestStatus.FAIL,
            Description="Failed to fetch sitemap.xml?browser_open=all",
            Expected_Result=len(self.site.internal_pages)
        )

class WebCrawler:
    def __init__(self, page: Page, base_url: str, max_depth=2, max_pages=100):
        self.page = page
        self.base_url = base_url if base_url.endswith('/') else base_url + '/'
        self.base_domain = self.get_domain(base_url)
        self.visited = set()
        self.to_visit = Queue()
        self.subdomains = set()
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.lock = threading.Lock()

    @staticmethod
    def get_domain(url: str) -> str:
        return urlparse(url).netloc

    def is_same_domain(self, url: str) -> bool:
        return self.get_domain(url).endswith(self.base_domain)

    @staticmethod
    def is_valid_url(url: str) -> bool:
        parsed_url = urlparse(url)
        return bool(parsed_url.scheme) and bool(parsed_url.netloc)

    def should_include(self, url: str) -> bool:
        return url.startswith(self.base_url)

    async def fetch_page(self, url: str) -> str:
        try:
            await self.page.goto(url)
            content = await self.page.content()
            return content
        except Exception as e:
            print(f"Error fetching {url}: {e}")
        return None

    def extract_links(self, content: str, current_url: str, current_depth: int):
        soup = BeautifulSoup(content, "html.parser")
        for link in soup.find_all("a", href=True):
            href = link['href']
            full_url = urljoin(current_url, href)
            if self.is_valid_url(full_url) and full_url not in self.visited:
                if self.is_same_domain(full_url) and self.should_include(full_url):
                    with self.lock:
                        if full_url not in self.visited:
                            self.visited.add(full_url)
                            self.to_visit.put((full_url, current_depth + 1))
                elif not self.is_same_domain(full_url):
                    with self.lock:
                        self.subdomains.add(self.get_domain(full_url))

    async def crawl_page(self, current_url: str, current_depth: int):
        if current_depth > self.max_depth:
            return

        content = await self.fetch_page(current_url)
        if content:
            self.extract_links(content, current_url, current_depth)

    async def crawl(self):
        while not self.to_visit.empty() and len(self.visited) < self.max_pages:
            current_url, current_depth = self.to_visit.get()
            await self.crawl_page(current_url, current_depth)

    def main(self):
        self.to_visit.put((self.base_url, 0))
        self.visited.add(self.base_url)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.crawl())

        return list(self.visited), list(self.subdomains)


#######################################################################################################
# class WebCrawler:
#     def __init__(self, base_url, max_depth=2, max_pages=1000):
#         self.base_url = base_url if base_url.endswith('/') else base_url + '/'
#         self.base_domain = self.get_domain(base_url)
#         self.visited = set()
#         self.to_visit = Queue()
#         self.subdomains = set()
#         self.max_depth = max_depth
#         self.max_pages = max_pages
#         self.lock = threading.Lock()
#
#     @staticmethod
#     def get_domain(url):
#         return urlparse(url).netloc
#
#     def is_same_domain(self, url):
#         return self.get_domain(url).endswith(self.base_domain)
#
#     @staticmethod
#     def is_valid_url(url):
#         parsed_url = urlparse(url)
#         return bool(parsed_url.scheme) and bool(parsed_url.netloc)
#
#     def should_include(self, url):
#         return url.startswith(self.base_url)
#
#     async def fetch_page(self, session, url):
#         try:
#             async with session.get(url) as response:
#                 if response.status == 200:
#                     return await response.text()
#         except Exception as e:
#             print(f"Error fetching {url}: {e}")
#         return None
#
#     def extract_links(self, content, current_url, current_depth):
#         soup = BeautifulSoup(content, "html.parser")
#         for link in soup.find_all("a", href=True):
#             href = link['href']
#             full_url = urljoin(current_url, href)
#             if self.is_valid_url(full_url) and full_url not in self.visited:
#                 if self.is_same_domain(full_url) and self.should_include(full_url):
#                     with self.lock:
#                         self.visited.add(full_url)
#                         self.to_visit.put((full_url, current_depth + 1))
#                 elif not self.is_same_domain(full_url):
#                     with self.lock:
#                         self.subdomains.add(self.get_domain(full_url))
#
#     async def crawl_page(self, session, current_url, current_depth):
#         if current_depth > self.max_depth:
#             return
#
#         content = await self.fetch_page(session, current_url)
#         if content:
#             self.extract_links(content, current_url, current_depth)
#
#     async def crawl(self):
#         async with ClientSession() as session:
#             while not self.to_visit.empty() and len(self.visited) < self.max_pages:
#                 current_url, current_depth = self.to_visit.get()
#                 await self.crawl_page(session, current_url, current_depth)
#
#     def main(self):
#         self.to_visit.put((self.base_url, 0))
#         self.visited.add(self.base_url)
#
#         loop = asyncio.get_event_loop()
#         loop.run_until_complete(self.crawl())
#
#         return list(self.visited), list(self.subdomains)
#
#
# class WebCrawlerTest(TestExecutionAsync):
#
#     def run_test(self) -> TestResult:
#         # Initialize the WebCrawler with the site URL
#         # crawler = WebCrawler(self.site.url)
#         crawler = WebCrawler(self.page.url)
#
#         # Start the crawling process
#         internal_pages, external_pages = crawler.main()
#
#         # Save the discovered pages to the site object
#         self.site.internal_pages.extend(internal_pages)
#         self.site.external_pages.extend(external_pages)
#
#         print("----<<<<", self.site)
#         print("Internal Pages:", len(internal_pages), len(set(internal_pages)))
#         print("Subdomains:", len(external_pages))
#
#         # Return the test result
#         return TestResult(
#             Name="Web Crawler Test",
#             Status=TestStatus.PASS,
#             Description="Discovered additional internal pages.",
#             Actual_Result=internal_pages
#         )
#
#     def run_comparison(self, results) -> ComparisonResult:
#         return ComparisonResult(
#             Name="Web Crawler Test",
#             Status=TestStatus.FAIL,
#             Description="Failed to fetch sitemap.xml?browser_open=all",
#             Expected_Result=len(self.site.internal_pages)
#         )
#############################################################################################
# class WebCrawlerTest(TestExecutionAsync):
#
#     def run_test(self) -> TestResult:
#         # Initialize the WebCrawler with the site URL
#         crawler = WebCrawler(self.site.url)
#
#         # Start the crawling process
#         internal_pages, external_pages = crawler.main()
#
#         # Save the discovered pages to the site object
#         self.site.internal_pages.extend(internal_pages)
#         self.site.external_pages.extend(external_pages)
#
#         print("----<<<<", self.site)
#         print("Internal Pages:", len(internal_pages), len(set(internal_pages)))
#         print("Subdomains:", len(external_pages))
#
#         # Return the test result
#         return TestResult(
#             Name="Web Crawler Test",
#             Status=TestStatus.PASS,
#             Description="Discovered additional internal pages.",
#             Actual_Result=internal_pages
#         )
#
#     def run_comparison(self, results) -> ComparisonResult:
#         return ComparisonResult(
#             Name="Web Crawler Test",
#             Status=TestStatus.FAIL,
#             Description="Failed to fetch sitemap.xml?browser_open=all",
#             Expected_Result=len(self.site.internal_pages)
#         )
#
#
# import asyncio
# from playwright.sync_api import sync_playwright
#
#
# class WebCrawler:
#     def __init__(self, base_url, max_depth=2, max_pages=1000):
#         self.base_url = base_url if base_url.endswith('/') else base_url + '/'
#         self.base_domain = self.get_domain(base_url)
#         self.visited = set()
#         self.to_visit = Queue()
#         self.subdomains = set()
#         self.max_depth = max_depth
#         self.max_pages = max_pages
#
#     @staticmethod
#     def get_domain(url):
#         return urlparse(url).netloc
#
#     def is_same_domain(self, url):
#         return self.get_domain(url).endswith(self.base_domain)
#
#     @staticmethod
#     def is_valid_url(url):
#         parsed_url = urlparse(url)
#         return bool(parsed_url.scheme) and bool(parsed_url.netloc)
#
#     def should_include(self, url):
#         return url.startswith(self.base_url)
#
#     async def fetch_page_async(self, url):
#         async with aiohttp.ClientSession() as session:
#             try:
#                 async with session.get(url) as response:
#                     if response.status == 200:
#                         return await response.text()
#             except Exception as e:
#                 print(f"Error fetching {url}: {e}")
#         return None
#
#     def fetch_page(self, url):
#         loop = asyncio.get_event_loop()
#         return loop.run_until_complete(self.fetch_page_async(url))
#
#     def extract_links(self, content, current_url, current_depth):
#         soup = BeautifulSoup(content, "html.parser")
#         for link in soup.find_all("a", href=True):
#             href = link['href']
#             full_url = urljoin(current_url, href)
#             if self.is_valid_url(full_url) and full_url not in self.visited:
#                 if self.is_same_domain(full_url) and self.should_include(full_url):
#                     self.visited.add(full_url)
#                     self.to_visit.put((full_url, current_depth + 1))
#                 elif not self.is_same_domain(full_url):
#                     self.subdomains.add(self.get_domain(full_url))
#
#     def crawl(self):
#         self.to_visit.put((self.base_url, 0))
#         self.visited.add(self.base_url)
#
#         while not self.to_visit.empty() and len(self.visited) < self.max_pages:
#             current_url, current_depth = self.to_visit.get()
#             if current_depth > self.max_depth:
#                 continue
#
#             content = self.fetch_page(current_url)
#             if content:
#                 self.extract_links(content, current_url, current_depth)
#
#     def main(self):
#         self.crawl()
#         return list(self.visited), list(self.subdomains)

# class WebCrawlerTest(TestExecutionAsync):
#
#     async def run_test(self) -> TestResult:
#         # Initialize the WebCrawler with the site URL
#         crawler = WebCrawler(self.site.url)
#
#         # Start the crawling process and wait for it to complete
#         internal_pages, external_pages = await crawler.main()
#
#         # Save the discovered pages to the site object
#         self.site.internal_pages.extend(internal_pages)
#         self.site.external_pages.extend(external_pages)
#
#         print("----<<<<", self.site)
#         print("Internal Pages:", len(internal_pages), len(set(internal_pages)))
#         print("Subdomains:", len(external_pages))
#
#         # Return the test result
#         return TestResult(
#             Name="Web Crawler Test",
#             Status=TestStatus.PASS,
#             Description="Discovered additional internal pages.",
#             Actual_Result=internal_pages
#         )
#
#     def run_comparison(self, results) -> ComparisonResult:
#         return ComparisonResult(
#             Name="Web Crawler Test",
#             Status=TestStatus.FAIL,
#             Description="Failed to fetch sitemap.xml?browser_open=all",
#             Expected_Result=len(self.site.internal_pages)
#         )
#
#
# class WebCrawler:
#     def __init__(self, base_url, max_depth=2, max_pages=100):
#         self.base_url = base_url if base_url.endswith('/') else base_url + '/'
#         self.base_domain = self.get_domain(base_url)
#         self.visited = set()
#         self.to_visit = Queue()
#         self.subdomains = set()
#         self.max_depth = max_depth
#         self.max_pages = max_pages
#
#     @staticmethod
#     def get_domain(url):
#         return urlparse(url).netloc
#
#     def is_same_domain(self, url):
#         return self.get_domain(url).endswith(self.base_domain)
#
#     @staticmethod
#     def is_valid_url(url):
#         parsed_url = urlparse(url)
#         return bool(parsed_url.scheme) and bool(parsed_url.netloc)
#
#     def should_include(self, url):
#         return url.startswith(self.base_url)
#
#     @staticmethod
#     async def fetch_page(session, url):
#         try:
#             async with session.get(url) as response:
#                 if response.status == 200:
#                     return await response.text()
#         except Exception as e:
#             print(f"Error fetching {url}: {e}")
#         return None
#
#     async def extract_links(self, content, current_url, current_depth):
#         soup = BeautifulSoup(content, "html.parser")
#         for link in soup.find_all("a", href=True):
#             href = link['href']
#             full_url = urljoin(current_url, href)
#             if self.is_valid_url(full_url) and full_url not in self.visited:
#                 if self.is_same_domain(full_url) and self.should_include(full_url):
#                     self.visited.add(full_url)
#                     await self.to_visit.put((full_url, current_depth + 1))
#                 elif not self.is_same_domain(full_url):
#                     self.subdomains.add(self.get_domain(full_url))
#
#     async def crawl(self):
#         async with aiohttp.ClientSession() as session:
#             await self.to_visit.put((self.base_url, 0))
#             self.visited.add(self.base_url)
#
#             while not self.to_visit.empty() and len(self.visited) < self.max_pages:
#                 current_url, current_depth = await self.to_visit.get()
#                 if current_depth > self.max_depth:
#                     continue
#
#                 content = await self.fetch_page(session, current_url)
#                 if content:
#                     await self.extract_links(content, current_url, current_depth)
#
#     async def main(self):
#         await self.crawl()
#         return list(self.visited), list(self.subdomains)
