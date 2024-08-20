# tests/test_sitemap_context_all.py
from Utilities.Data_Structures import TestResult, TestStatus, ComparisonResult
from Contracts.test_contract import TestExecution
import requests
from urllib.parse import urljoin
import xml.etree.ElementTree as ET


class SitemapContextAllTest(TestExecution):
    url_context_all = []

    def run_test(self):
        sitemap_url = urljoin(self.site.url, "sitemap.xml?browser_open=all")
        response = requests.get(sitemap_url)

        if response.status_code == 200:
            tree = ET.ElementTree(ET.fromstring(response.content))
            urls = [url.text for url in tree.findall(".//loc")]

            # Add new URLs to internal_pages if not already present
            self.url_context_all = [url for url in urls if url not in self.site.env.prod.internal_pages]
            self.site.internal_pages.extend(self.url_context_all)  # Save internal pages

            return TestResult(
                Name="Sitemap Context All Test",
                Status=TestStatus.PASS,
                Description="Successfully fetched sitemap.xml?browser_open=all",
                Actual_Result=self.url_context_all
            )
        else:
            return TestResult(
                Name="Sitemap Context All Test",
                Status=TestStatus.FAIL,
                Description="Failed to fetch sitemap.xml?browser_open=all",
                Actual_Result=[]
            )

    def run_comparison(self, results):
        return ComparisonResult(
            Name="Sitemap Context All Test",
            Status=TestStatus.FAIL,
            Description="Failed to fetch sitemap.xml?browser_open=all",
            Expected_Result=len(self.url_context_all)
        )
