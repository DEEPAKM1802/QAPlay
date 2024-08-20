from Utilities.Data_Structures import TestResult, ComparisonResult
from Utilities.FilePath_Handler import OutputHandler
from abc import ABC, abstractmethod


class TestExecution(ABC):

    def __init__(self, subscription, page):
        self.subscription = subscription
        self.page = page
        self.site = None
        self.env = None
        self.test_execution()

    @abstractmethod
    def run_test(self) -> TestResult:
        pass

    @abstractmethod
    def run_comparison(self, results) -> ComparisonResult:
        pass

    def test_execution(self):
        for env_name, site in self.subscription.env:
            if site is not None:
                self.site = site
                self.env = env_name
                test_result = self.run_test()
                OutputHandler.save_test_result(self.subscription.name, env_name, test_result)
        self.save_test_comparison()

    def save_test_comparison(self):
        results = OutputHandler.get_test_results(self.subscription.name)
        comparison_result = self.run_comparison(results)
        OutputHandler.save_comparison_result(self.subscription.name, comparison_result)

    # def generate_report(self):
    #     file_paths = OutputHandler.get_file_paths(subscription.name)
    #     generate_html_report(file_paths, subscription.name)
