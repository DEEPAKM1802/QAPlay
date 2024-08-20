import time

from Contracts.test_contract import TestExecution, TestExecutionAsync
from Utilities.Data_Structures import TestResult, TestStatus, ComparisonResult

# class Errors(TestExecution):
#
#     def run_test(self):
#         # url = self.site.url
#         error_logs = []
#         print(self.site.internal_pages)
#         for url in self.site.internal_pages:
#             self.driver.get(url)
#             logs = self.driver.get_log('browser') + self.driver.get_log('driver')
#             print("logs---->>", logs)
#             for log in logs:
#                 if log['level'] in ['ERROR', 'SEVERE']:
#                     error_logs.append(log)
#
#         if error_logs:
#             return TestResult(
#                 Name="Console Errors",
#                 Status=TestStatus.FAIL,
#                 Description="Console Error Fail",
#                 Actual_Result=error_logs
#             )
#
#         else:
#             return TestResult(
#                 Name="Console Errors",
#                 Status=TestStatus.PASS,
#                 Description="Console Error Pass",
#                 Actual_Result=error_logs
#             )
#
#     def run_comparison(self, results):
#         return ComparisonResult(
#             Name="Console Errors",
#             Status=TestStatus.PASS,
#             Description="Console Error Compare",
#             Expected_Result=[]
#         )

# import asyncio
# from concurrent.futures import ThreadPoolExecutor
# from selenium import webdriver
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#
#
# class Errors(TestExecutionAsync):
#
#     def __init__(self, subscription, setup):
#         super().__init__(subscription, setup)
#         self.executor = ThreadPoolExecutor(max_workers=5)  # Adjust max_workers based on your needs
#
#     async def run_test(self):
#         error_logs = []
#
#         async def fetch_errors(url):
#             loop = asyncio.get_running_loop()
#             driver = self.driver
#             await loop.run_in_executor(self.executor, driver.get, url)
#             logs = await loop.run_in_executor(self.executor, driver.get_log, 'browser')
#             logs += await loop.run_in_executor(self.executor, driver.get_log, 'driver')
#             return [log for log in logs if log['level'] in ['ERROR', 'SEVERE']]
#
#         tasks = [fetch_errors(url) for url in self.site.internal_pages]
#         results = await asyncio.gather(*tasks)
#
#         for result in results:
#             error_logs.extend(result)
#
#         if error_logs:
#             return TestResult(
#                 Name="Console Errors",
#                 Status=TestStatus.FAIL,
#                 Description="Console Error Fail",
#                 Actual_Result=error_logs
#             )
#         else:
#             return TestResult(
#                 Name="Console Errors",
#                 Status=TestStatus.PASS,
#                 Description="Console Error Pass",
#                 Actual_Result=error_logs
#             )
#
#     def run_comparison(self, results):
#         return ComparisonResult(
#             Name="Console Errors",
#             Status=TestStatus.PASS,
#             Description="Console Error Compare",
#             Expected_Result=[]
#         )
#
#     async def execute(self):
#         await self.execute_tests()

import asyncio
from playwright.async_api import async_playwright

# class Errors(TestExecutionAsync):
#
#     async def run_test(self):
#         error_logs = []
#
#         async def fetch_errors(page, url):
#             try:
#                 await page.goto(url)
#                 logs = await page.evaluate("() => console.log")  # Use page.evaluate to get console logs
#                 print("logs--->", logs)
#                 for log in logs:
#                     if log['level'] in ['error']:
#                         error_logs.append({'url': url, 'log': log})
#             except Exception as e:
#                 error_logs.append({'url': url, 'error': str(e)})
#
#         async with async_playwright() as p:
#             browser = await p.chromium.launch()
#             browser_open = await browser.new_context()
#             pages = [await browser_open.new_page() for _ in range(min(len(self.site.internal_pages), 10))]
#
#             # Divide URLs among pages
#             tasks = []
#             for i, page in enumerate(pages):
#                 url_batch = self.site.internal_pages[i::len(pages)]
#                 for url in url_batch:
#                     tasks.append(fetch_errors(page, url))
#
#             await asyncio.gather(*tasks)
#             await browser.close()
#
#         if error_logs:
#             return TestResult(
#                 Name="Console Errors",
#                 Status=TestStatus.FAIL,
#                 Description="Console Error Fail",
#                 Actual_Result=error_logs
#             )
#         else:
#             return TestResult(
#                 Name="Console Errors",
#                 Status=TestStatus.PASS,
#                 Description="Console Error Pass",
#                 Actual_Result=error_logs
#             )
#
#     def run_comparison(self, results):
#         return ComparisonResult(
#             Name="Console Errors",
#             Status=TestStatus.PASS,
#             Description="Console Error Compare",
#             Expected_Result=[]
#         )
#
# # You will need to modify your test run configuration to support asynchronous execution


# class Errors(TestExecutionAsync):
#
#     async def run_test(self):
#         error_logs = {}
#
#         def handle_console_log(msg):
#             print("msg--->>>", msg)
#             if msg.type in ['error', 'warning', 'ERROR', 'Error', 'SEVERE', 'severe']:
#                 error_logs[current_url].append(msg.text)
#                 # error_logs.append({'url': current_url, 'log': msg.text})
#
#         async def fetch_errors(page, url):
#             global current_url
#             current_url = url
#             try:
#                 # Attach console log handler before navigation
#                 page.on('console', handle_console_log)
#
#                 # Navigate and wait for the network to be idle
#                 await page.goto(url, wait_until='networkidle')
#                 await page.wait_for_timeout(1000)  # Adjust timeout as necessary
#
#             except Exception as e:
#                 error_logs[current_url].append(f'Navigation error: {str(e)}')
#                 # error_logs.append({'url': url, 'error': f'Navigation error: {str(e)}'})
#             # finally:
#             #     # Remove the console log handler after the page is closed
#             #     page.off('console', handle_console_log)
#
#         async with async_playwright() as p:
#             browser = await p.chromium.launch()
#             browser_open = await browser.new_context()
#             pages = [await browser_open.new_page() for _ in range(min(len(self.site.internal_pages), 10))]
#
#             # Divide URLs among pages
#             tasks = []
#             for i, page in enumerate(pages):
#                 url_batch = self.site.internal_pages[i::len(pages)]
#                 for url in url_batch:
#                     tasks.append(fetch_errors(page, url))
#
#             await asyncio.gather(*tasks)
#             await browser.close()
#
#         if error_logs:
#             return TestResult(
#                 Name="Console Errors",
#                 Status=TestStatus.FAIL,
#                 Description="Console Error Fail",
#                 Actual_Result=error_logs
#             )
#         else:
#             return TestResult(
#                 Name="Console Errors",
#                 Status=TestStatus.PASS,
#                 Description="Console Error Pass",
#                 Actual_Result=error_logs
#             )
#
#     def run_comparison(self, results):
#         return ComparisonResult(
#             Name="Console Errors",
#             Status=TestStatus.PASS,
#             Description="Console Error Compare",
#             Expected_Result=[]
#         )


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from playwright.async_api import async_playwright
import asyncio


class Errors(TestExecutionAsync):

    async def run_test(self):
        error_logs = {}
        lock = asyncio.Lock()

        async def handle_console_log(msg, url):
            if msg.type in ['error', 'warning', 'ERROR', 'Error', 'SEVERE', 'severe']:
                async with lock:
                    if url not in error_logs:
                        error_logs[url] = []
                    error_logs[url].append(msg.text)

        async def fetch_errors(page, url):
            try:
                # Attach console log handler before navigation
                page.on('console', lambda msg: handle_console_log(msg, url))

                # Navigate and wait for the network to be idle
                await page.goto(url, wait_until='networkidle')
                await page.wait_for_timeout(1000)  # Adjust timeout as necessary

            except Exception as e:
                async with lock:
                    if url not in error_logs:
                        error_logs[url] = []
                    error_logs[url].append(f'Navigation error: {str(e)}')

        async with async_playwright() as p:
            browser = await p.chromium.launch()
            context = await browser.new_context()
            pages = [await context.new_page() for _ in range(min(len(self.site.internal_pages), 10))]

            # Divide URLs among pages
            tasks = []
            for i, page in enumerate(pages):
                url_batch = self.site.internal_pages[i::len(pages)]
                for url in url_batch:
                    tasks.append(fetch_errors(page, url))

            await asyncio.gather(*tasks)
            await browser.close()

        if error_logs:
            return TestResult(
                Name="Console Errors",
                Status=TestStatus.FAIL,
                Description="Console Error Fail",
                Actual_Result=error_logs
            )
        else:
            return TestResult(
                Name="Console Errors",
                Status=TestStatus.PASS,
                Description="Console Error Pass",
                Actual_Result=error_logs
            )

    def run_comparison(self, results):
        return ComparisonResult(
            Name="Console Errors",
            Status=TestStatus.PASS,
            Description="Console Error Compare",
            Expected_Result=[]
        )
