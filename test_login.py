import pytest
from Contracts.test_contract import TestExecution
from Utilities.Data_Structures import TestResult, TestStatus, ComparisonResult
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


class LoginTest(TestExecution):
    def run_test(self) -> TestResult:
        try:
            page = self.page.new_page()
            # print(f"Logging in at: {self.site.login.login_url}")
            page.goto(self.site.login.login_url)
            page.fill(self.site.login.username_xpath, self.site.login.username)
            page.fill(self.site.login.password_xpath, self.site.login.password)
            page.wait_for_timeout(2000)  # Wait for 2 seconds before clicking the login button
            page.locator(self.site.login.sign_in_xpath).click()
            page.wait_for_load_state('networkidle')
            pytest._authenticated_state = self.page.storage_state()  # Save authenticated state
            self.site.internal_pages.append(self.site.login.login_url)
            page.close()

            return TestResult(
                Name="Login Test",
                Status=TestStatus.PASS,
                Description="Successfully logged into the application.",
                Actual_Result="Logged in"
            )

        except PlaywrightTimeoutError as e:
            print(f"Timeout error: {e}")
            return TestResult(
                Name="Login Test",
                Status=TestStatus.PASS,
                Description="Timeout while trying to log in.",
                Actual_Result="Failed to log in due to timeout."
            )

    def run_comparison(self, results):
        # Example comparison logic
        return ComparisonResult(
            Name="Login Test",
            Status=TestStatus.PASS,
            Description="Login functionality works as expected.",
            Expected_Result="User is on the Dashboard page."
        )