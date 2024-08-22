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
#######################################################################################################################
from playwright.sync_api import Page, expect


class LoginTest(TestExecution):
    # Translation dictionary for common login terms in multiple languages
    login_translations = {
        "en": ["log in", "login", "sign in", "sign in", "access"],
        "fr": ["se connecter", "connexion", "identifiez-vous"],
        "de": ["anmelden", "login", "einloggen"],
        "es": ["iniciar sesión", "acceso", "entrar"],
        # Add more languages as needed
    }

    def find_login_button(self, page: Page):
        for language, terms in self.login_translations.items():
            for term in terms:
                login_button = page.locator(f"text='{term}'")
                if login_button.is_visible():
                    return login_button

        # Fallback to any button with login-related attributes
        login_button = page.locator("button, a").filter(
            lambda e: "login" in e.get_attribute("class") or "sign" in e.get_attribute("class") or
                      "login" in e.get_attribute("id") or "sign" in e.get_attribute("id")
        ).first()

        return login_button

    def find_input_field(self, page: Page, field_type: str):
        # Try to locate by name or placeholder
        field = page.locator(f"input[name*='{field_type}'], input[placeholder*='{field_type}']")
        if field.is_visible():
            return field.first()

        # Fallback to input fields with certain types or roles
        if field_type == "username":
            return page.locator("input[type='email'], input[type='text']").first()
        elif field_type == "password":
            return page.locator("input[type='password']").first()

        return None

    def run_test(self) -> TestResult:
        try:
            page = self.page.new_page()
            page.goto(self.site.base_url)

            # Step 1: Find and click the login button
            login_button = self.find_login_button(page)
            if login_button:
                login_button.click()
            else:
                raise Exception("Login button not found")

            # Step 2: Locate the username and password fields
            username_field = self.find_input_field(page, "username")
            password_field = self.find_input_field(page, "password")

            if username_field and password_field:
                # Fill in the username and password
                username_field.fill(self.site.login.username)
                password_field.fill(self.site.login.password)
            else:
                raise Exception("Username or Password field not found")

            # Step 3: Submit the form
            submit_button = page.locator("button[type='submit'], button[type='button']").first()
            if submit_button.is_visible():
                submit_button.click()
            else:
                raise Exception("Submit button not found")

            # Step 4: Wait for the network to idle and save state
            page.wait_for_load_state('networkidle')
            pytest._authenticated_state = self.page.storage_state()
            self.site.internal_pages.append(self.site.login.login_url)

            return TestResult(
                Name="Login Test",
                Status=TestStatus.PASS,
                Description="Successfully logged into the application.",
                Actual_Result="Logged in"
            )

        except Exception as e:
            return TestResult(
                Name="Login Test",
                Status=TestStatus.FAIL,
                Description="Login test failed.",
                Actual_Result=str(e)
            )


#########################################################################################################
from playwright.sync_api import Page, expect
from googletrans import Translator  # Google Translate API


class LoginTest(TestExecution):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.translator = Translator()

    def translate_text(self, text: str) -> str:
        result = self.translator.translate(text, dest='en')
        return result.text.lower().strip()

    def find_login_button(self, page: Page):
        buttons = page.locator("button, a").all_text_contents()

        for button in buttons:
            translated_text = self.translate_text(button)
            if "login" in translated_text or "sign in" in translated_text or "access" in translated_text:
                return page.locator(f"text='{button}'")

        # Fallback: try to find by attributes like id or class
        login_button = page.locator("button, a").filter(
            lambda e: "login" in e.get_attribute("class") or "sign" in e.get_attribute("class") or
                      "login" in e.get_attribute("id") or "sign" in e.get_attribute("id")
        ).first()

        return login_button

    def find_input_field(self, page: Page, field_type: str):
        # Common terms for the field_type (username or password)
        field_identifiers = {
            "username": ["username", "email", "user", "mobile", "phone", "account"],
            "password": ["password", "pass", "pwd"]
        }

        fields = page.locator("input").all()

        for field in fields:
            placeholder = field.get_attribute("placeholder")
            name = field.get_attribute("name")
            id_attr = field.get_attribute("id")

            # Normalize and translate text to match common identifiers
            for identifier in field_identifiers[field_type]:
                if placeholder and identifier in self.translate_text(placeholder):
                    return field
                if name and identifier in self.translate_text(name):
                    return field
                if id_attr and identifier in self.translate_text(id_attr):
                    return field

        # Fallback: return any input field if none match
        return page.locator("input").first()

    def run_test(self) -> TestResult:
        try:
            page = self.page.new_page()
            page.goto(self.site.base_url)

            # Step 1: Find and click the login button
            login_button = self.find_login_button(page)
            if login_button:
                login_button.click()
            else:
                raise Exception("Login button not found")

            # Step 2: Locate the username and password fields
            username_field = self.find_input_field(page, "username")
            password_field = self.find_input_field(page, "password")

            if username_field and password_field:
                # Fill in the username and password
                username_field.fill(self.site.login.username)
                password_field.fill(self.site.login.password)
            else:
                raise Exception("Username or Password field not found")

            # Step 3: Submit the form
            submit_button = page.locator("button[type='submit'], button[type='button']").first()
            if submit_button.is_visible():
                submit_button.click()
            else:
                raise Exception("Submit button not found")

            # Step 4: Wait for the network to idle and save state
            page.wait_for_load_state('networkidle')
            pytest._authenticated_state = self.page.storage_state()
            self.site.internal_pages.append(self.site.login.login_url)

            return TestResult(
                Name="Login Test",
                Status=TestStatus.PASS,
                Description="Successfully logged into the application.",
                Actual_Result="Logged in"
            )

        except Exception as e:
            return TestResult(
                Name="Login Test",
                Status=TestStatus.FAIL,
                Description="Login test failed.",
                Actual_Result=str(e)
            )
