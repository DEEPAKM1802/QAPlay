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
