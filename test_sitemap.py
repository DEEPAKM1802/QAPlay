# tests/test_sitemap.py
from Utilities.Data_Structures import TestResult, TestStatus, ComparisonResult
from Contracts.test_contract import TestExecution
import requests
from urllib.parse import urljoin
import xml.etree.ElementTree as ET


class SitemapTest(TestExecution):

    def run_test(self):
        sitemap_url = urljoin(self.site.url, "sitemap.xml")
        response = requests.get(sitemap_url)

        if response.status_code == 200:
            tree = ET.ElementTree(ET.fromstring(response.content))
            self.urls_sitemap = [url.text for url in tree.findall(".//loc")]
            self.site.internal_pages.extend(self.urls_sitemap)  # Save internal pages
            return TestResult(
                Name="Sitemap Test",
                Status=TestStatus.PASS,
                Description="Successfully fetched sitemap.xml",
                Actual_Result=len(self.urls_sitemap)
            )
        else:
            return TestResult(
                Name="Sitemap Test",
                Status=TestStatus.FAIL,
                Description="Failed to fetch sitemap.xml",
                Actual_Result=[]
            )

    def run_comparison(self, results):
        return ComparisonResult(
            Name="Sitemap Test",
            Status=TestStatus.FAIL,
            Description="Failed to fetch sitemap.xml",
            Expected_Result=len(self.urls_sitemap)
        )
