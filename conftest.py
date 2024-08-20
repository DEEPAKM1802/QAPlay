import pytest
from Utilities.TOMLConfigLader import ConfigLoader
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def playwright():
    with sync_playwright() as playwright_instance:
        yield playwright_instance


@pytest.fixture(scope="session")
def browser(playwright):
    # chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"  # Update this path
    browser = playwright.chromium.launch(channel="chrome", headless=False)
    yield browser
    browser.close()


@pytest.fixture(scope="module")
def context(browser):
    context = browser.new_context()
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context):
    # context = browser.new_context(storage_state=pytest._authenticated_state)
    page = context.new_page()
    yield page
    page.close()


# Define the pytest_generate_tests hook to generate test cases
def pytest_generate_tests(metafunc):
    sub = ConfigLoader()
    print(sub)
    if 'subscription' in metafunc.fixturenames:
        # Generate test cases based on the test_data list
        metafunc.parametrize('subscription', sub, scope='module')
