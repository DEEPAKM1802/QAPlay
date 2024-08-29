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








def test_console_errors(self):
    page = self.page.new_page()
    page.goto(self.site.url)

    # Listen for console messages
    def handle_console_msg(msg):
        if msg.type == 'error':
            print(f"Console error: {msg.text}")
            self.console_errors.append(msg.text)

    page.on("console", handle_console_msg)
    page.goto(self.site.url)

    # Check if there are any console errors
    if self.console_errors:
        return TestResult(
            Name="Console Errors Test",
            Status=TestStatus.FAIL,
            Description="Console errors found on the page.",
            Actual_Result=f"Errors: {self.console_errors}"
        )
    else:
        return TestResult(
            Name="Console Errors Test",
            Status=TestStatus.PASS,
            Description="No console errors found.",
            Actual_Result="No errors"
        )












def test_performance_errors(self):
    page = self.page.new_page()
    page.goto(self.site.url)

    # Listen for request and response failures
    def handle_request_failed(request):
        print(f"Request failed: {request.url}")
        self.failed_requests.append(request.url)

    def handle_response(response):
        if response.status >= 400:
            print(f"Error in response: {response.url} with status code {response.status}")
            self.failed_responses.append((response.url, response.status))

    page.on("requestfailed", handle_request_failed)
    page.on("response", handle_response)
    page.goto(self.site.url)

    # Check if there are any failed requests or error responses
    if self.failed_requests or self.failed_responses:
        return TestResult(
            Name="Performance Errors Test",
            Status=TestStatus.FAIL,
            Description="API or script errors found in the performance tab.",
            Actual_Result=f"Failed requests: {self.failed_requests}, Error responses: {self.failed_responses}"
        )
    else:
        return TestResult(
            Name="Performance Errors Test",
            Status=TestStatus.PASS,
            Description="No API or script errors found.",
            Actual_Result="No errors"
        )







def test_404_response(self):
    page = self.page.new_page()
    
    # Capture the response of the page
    response = page.goto(self.site.url)

    # Check if the response status is 404
    if response.status == 404:
        return TestResult(
            Name="404 Response Code Test",
            Status=TestStatus.FAIL,
            Description="Page returned a 404 error.",
            Actual_Result="404 error found"
        )
    else:
        return TestResult(
            Name="404 Response Code Test",
            Status=TestStatus.PASS,
            Description="Page loaded successfully without 404 error.",
            Actual_Result=f"Response code: {response.status}"
        )









from playwright.sync_api import Page, TimeoutError, Error

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self, url: str, timeout: int = 30000):
        try:
            self.page.goto(url, timeout=timeout)
        except TimeoutError:
            print(f"Timeout while navigating to {url}.")
        except Error as e:
            print(f"Failed to navigate to {url}: {str(e)}")

    def locator(self, selector: str):
        try:
            return self.page.locator(selector)
        except Error as e:
            print(f"Failed to find locator '{selector}': {str(e)}")
            return None

    def click(self, selector: str):
        try:
            self.page.click(selector)
        except TimeoutError:
            print(f"Timeout while clicking on '{selector}'.")
        except Error as e:
            print(f"Failed to click on '{selector}': {str(e)}")

    def fill(self, selector: str, text: str):
        try:
            self.page.fill(selector, text)
        except TimeoutError:
            print(f"Timeout while filling '{selector}' with '{text}'.")
        except Error as e:
            print(f"Failed to fill '{selector}' with '{text}': {str(e)}")

    def select_option(self, selector: str, value: str):
        try:
            self.page.select_option(selector, value)
        except TimeoutError:
            print(f"Timeout while selecting option '{value}' in '{selector}'.")
        except Error as e:
            print(f"Failed to select option '{value}' in '{selector}': {str(e)}")

    def get_text(self, selector: str):
        try:
            return self.page.text_content(selector)
        except TimeoutError:
            print(f"Timeout while getting text from '{selector}'.")
            return None
        except Error as e:
            print(f"Failed to get text from '{selector}': {str(e)}")
            return None

    def is_visible(self, selector: str):
        try:
            return self.page.is_visible(selector)
        except TimeoutError:
            print(f"Timeout while checking visibility of '{selector}'.")
            return False
        except Error as e:
            print(f"Failed to check visibility of '{selector}': {str(e)}")
            return False

    def wait_for_selector(self, selector: str, timeout: int = 30000):
        try:
            return self.page.wait_for_selector(selector, timeout=timeout)
        except TimeoutError:
            print(f"Timeout while waiting for selector '{selector}'.")
            return None
        except Error as e:
            print(f"Failed to wait for selector '{selector}': {str(e)}")
            return None

    # Add more methods as needed...

# Example usage in your test case
class GDPRPopupTest(TestExecution):
    gdpr_titles = [
        "We value your privacy",
        "Privacy Preference",
        # ... other titles ...
    ]

    def find_gdpr_popup(self, base_page: BasePage):
        for title in self.gdpr_titles:
            print(f"Checking for GDPR pop-up with title: {title}")
            popup = base_page.locator(f"text={title}:visible")
            if popup and base_page.is_visible(f"text={title}:visible"):
                print(f"GDPR pop-up detected with title: {title}")
                return True
        return False

    def run_test(self) -> TestResult:
        try:
            base_page = BasePage(self.page.new_page())
            base_page.goto(self.site.url)

            gdpr_popup_detected = self.find_gdpr_popup(base_page)
            if gdpr_popup_detected:
                return TestResult(
                    Name="GDPR Popup Test",
                    Status=TestStatus.PASS,
                    Description="GDPR pop-up detected.",
                    Actual_Result="GDPR pop-up found with one of the known titles."
                )
            else:
                return TestResult(
                    Name="GDPR Popup Test",
                    Status=TestStatus.FAIL,
                    Description="No GDPR pop-up detected.",
                    Actual_Result="No GDPR pop-up found with the known titles."
                )

        except Exception as e:
            return TestResult(
                Name="GDPR Popup Test",
                Status=TestStatus.FAIL,
                Description="GDPR Popup Test failed.",
                Actual_Result=str(e)
            )
