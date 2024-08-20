import pytest
from TestCases.test_login import LoginTest
from TestCases.test_sample1 import Sample1
from TestCases.test_sitemap import SitemapTest
from Utilities.FilePath_Handler import OutputHandler
from Utilities.Report_HTML import generate_html_report
from Utilities.TOMLConfigLader import ConfigLoader


def test_login(subscription, context):
    print(f"Testing login: {subscription.name}")
    LoginTest(subscription, context)
#
#
# def test_sample1(subscription, page):
#     print(f"Testing sample: {subscription.name}")
#     Sample1(subscription, page)


# def test_sample2(subscription, page):
#     print(f"Testing sample: {subscription.name}")
#     Sample1(subscription, page)

# def teardown_module(subscription):
#     print(subscription)
#     file_paths = OutputHandler.get_file_paths(subscription.name)
#     generate_html_report(file_paths, subscription.name)
