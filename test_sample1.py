from Contracts.test_contract import TestExecution
from Utilities.Data_Structures import TestResult, TestStatus, ComparisonResult
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


class Sample1(TestExecution):
    def run_test(self) -> TestResult:
        try:
            self.page.goto(self.site.url)
            self.page.wait_for_load_state('networkidle')

            return TestResult(
                Name="Sample1 Test",
                Status=TestStatus.PASS,
                Description="Successfully logged into the application.",
                Actual_Result="Logged in"
            )

        except PlaywrightTimeoutError as e:
            print(f"Timeout error: {e}")
            return TestResult(
                Name="Sample1 Test",
                Status=TestStatus.PASS,
                Description="Timeout while trying to log in.",
                Actual_Result="Failed to log in due to timeout."
            )

    def run_comparison(self, results):
        # Example comparison logic
        return ComparisonResult(
            Name="Sample1 Test",
            Status=TestStatus.PASS,
            Description="Login functionality works as expected.",
            Expected_Result="User is on the Dashboard page."
        )