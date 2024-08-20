import requests
from Contracts.test_contract import TestExecution
from Utilities.Data_Structures import TestResult, TestStatus, ComparisonResult


class PageNotFound(TestExecution):

    def run_test(self):
        requests.get(str(self.site.url) + "404")
        if requests.status_codes != (404, 301):
            return TestResult(
                Name="Page Not Found",
                Status=TestStatus.FAIL,
                Description="404 Fail",
                Actual_Result=requests.status_codes
            )
        else:
            return TestResult(
                Name="Page Not Found",
                Status=TestStatus.PASS,
                Description="404 Pass",
                Actual_Result=requests.status_codes
            )

    def run_comparison(self, results):
        # print("results", results)
        return ComparisonResult(
            Name="Page Not Found",
            Status=TestStatus.PASS,
            Description="Page Error Compare",
            Expected_Result=[]
        )
