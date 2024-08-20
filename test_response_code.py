from abc import ABC

import requests
from selenium.webdriver.common.by import By

from Contracts.test_contract import TestExecution
from Utilities.Data_Structures import TestResult, TestStatus, ComparisonResult


class ResponseCode(TestExecution):

    def run_test(self):
        # self.driver.get(self.site.url)
        # hyperlinks = self.driver.find_elements(By.TAG_NAME, "a")
        # links = [link.get_attribute('href') for link in hyperlinks if link.get_attribute('href')]
        responses = {}
        for link in self.site.internal_pages:
            requests.get(str(link))
            if requests.status_codes != 200:
                responses[link] = requests.status_codes
        if responses:
            return TestResult(
                Name="Response Code",
                Status=TestStatus.FAIL,
                Description="Response Code Fail",
                Actual_Result=responses
            )
        else:
            return TestResult(
                Name="Response Code",
                Status=TestStatus.PASS,
                Description="Response Code Pass",
                Actual_Result=responses
            )

    def run_comparison(self, results):
        return ComparisonResult(
            Name="Response Code",
            Status=TestStatus.PASS,
            Description="Response Code Pass",
            Expected_Result=[]
        )
