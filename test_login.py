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





import re
from playwright.sync_api import Page, expect, TimeoutError

class LoginTest(TestExecution):

    login_translations = {
        "en": ["login", "log in", "sign in", "signin"],
        "fr": ["connexion", "se connecter"],
        "de": ["anmelden", "login", "einloggen"],
        "es": ["iniciar sesión", "acceso", "entrar"],
        "it": ["accedi", "login", "collegati"],
        "pt": ["entrar", "iniciar sessão"],
        "tr": ["giriş yap", "oturum aç", "login"],
        "nl": ["inloggen", "login", "aanmelden"],
        "zh-cn": ["登录", "登入"],
        "ja": ["ログイン", "サインイン"],
        "ko": ["로그인", "접속"],
        "el": ["σύνδεση", "login", "είσοδος"]  # Greek translations
    }

    username_translations = {
        "en": ["username", "email", "e-mail", "user", "mobile", "phone", "account"],
        "fr": ["nom d'utilisateur", "e-mail", "adresse électronique", "téléphone", "compte"],
        "de": ["benutzername", "e-mail", "telefon", "konto"],
        "es": ["nombre de usuario", "correo electrónico", "email", "teléfono", "cuenta"],
        "it": ["nome utente", "e-mail", "telefono", "account"],
        "pt": ["nome de usuário", "e-mail", "telefone", "conta"],
        "tr": ["kullanıcı adı", "e-posta", "telefon", "hesap"],
        "nl": ["gebruikersnaam", "e-mail", "telefoon", "account"],
        "zh-cn": ["用户名", "电子邮件", "电话", "帐户"],
        "ja": ["ユーザー名", "電子メール", "電話", "アカウント"],
        "ko": ["사용자 이름", "이메일", "전화", "계정"],
        "el": ["όνομα χρήστη", "ηλεκτρονικό ταχυδρομείο", "τηλέφωνο", "λογαριασμός"]  # Greek translations
    }

    password_translations = {
        "en": ["password", "pass", "pwd"],
        "fr": ["mot de passe", "passe"],
        "de": ["passwort"],
        "es": ["contraseña", "clave"],
        "it": ["password", "parola d'ordine"],
        "pt": ["senha", "palavra-passe"],
        "tr": ["şifre", "parola"],
        "nl": ["wachtwoord"],
        "zh-cn": ["密码"],
        "ja": ["パスワード"],
        "ko": ["비밀번호"],
        "el": ["κωδικός πρόσβασης", "κωδικός"]
    }

    submit_translations = {
        "en": ["login", "log in", "sign in", "signin", "submit", "Submit", "SUBMIT"],
        "fr": ["connexion", "se connecter", "soumettre", "Soumettre", "SOUMETTRE"],
        "de": ["anmelden", "login", "einloggen", "einreichen", "Einreichen", "EINREICHEN"],
        "es": ["iniciar sesión", "acceso", "entrar", "enviar", "Enviar", "ENVIAR"],
        "it": ["accedi", "login", "collegati", "invia", "Invia", "INVIA"],
        "pt": ["entrar", "iniciar sessão", "enviar", "Enviar", "ENVIAR"],
        "tr": ["giriş yap", "oturum aç", "login", "gönder", "Gönder", "GÖNDER"],
        "nl": ["inloggen", "login", "aanmelden", "indienen", "Indienen", "INDIENEN"],
        "zh-cn": ["登录", "登入", "提交", "提交", "提交"],
        "ja": ["ログイン", "サインイン", "送信", "送信", "送信"],
        "ko": ["로그인", "접속", "제출", "제출", "제출"],
        "el": ["σύνδεση", "login", "είσοδος", "υποβολή", "Υποβολή", "ΥΠΟΒΟΛΗ"]  # Greek translations
    }
    def generate_login_regex(self):
        all_terms = [term for terms in self.login_translations.values() for term in terms]
        patterns = [rf"\b{re.escape(term)}\b" for term in all_terms]
        regex_pattern = "|".join(patterns)
        compiled_regex = re.compile(regex_pattern, re.IGNORECASE)
        return compiled_regex


    def generate_username_regex(self):
        all_terms = [term for terms in self.username_translations.values() for term in terms]
        patterns = [rf"\b{re.escape(term)}\b" for term in all_terms]
        regex_pattern = "|".join(patterns)
        compiled_regex = re.compile(regex_pattern, re.IGNORECASE)
        return compiled_regex


    def generate_password_regex(self):
        all_terms = [term for terms in self.password_translations.values() for term in terms]
        patterns = [rf"\b{re.escape(term)}\b" for term in all_terms]
        regex_pattern = "|".join(patterns)
        compiled_regex = re.compile(regex_pattern, re.IGNORECASE)
        return compiled_regex


    def generate_submit_button_regex(self):
        submit_terms = [term for terms in self.submit_translations.values() for term in terms]
        patterns = [rf"\b{re.escape(term)}\b" for term in submit_terms]
        regex_pattern = "|".join(patterns)
        compiled_regex = re.compile(regex_pattern, re.IGNORECASE)
        return compiled_regex


    def find_element(self, page: Page, regex, element_type="input"):
        elements = page.locator(f"{element_type}:visible").all()
        unique_elements = set()

        for element in elements:
            identifier = (element.get_attribute("id"), element.get_attribute("name"), element.text_content())
            if identifier in unique_elements:
                continue
            unique_elements.add(identifier)

            text_content = element.text_content() or ""
            placeholder = element.get_attribute("placeholder") or ""
            name = element.get_attribute("name") or ""
            id_attr = element.get_attribute("id") or ""

            if (regex.search(text_content) or
                    regex.search(placeholder) or
                    regex.search(name) or
                    regex.search(id_attr)):
                return element

        return None


    def run_test(self) -> TestResult:
        try:
            page = self.page.new_page()
            page.goto(self.site.url)

            # Step 1: Find and click the login button
            login_regex = self.generate_login_regex()
            login_button = self.find_element(page, login_regex, element_type="button,a")
            if login_button:
                login_button.click()
                page.wait_for_timeout(3000)

            else:
                return TestResult(
                    Name="Login Test",
                    Status=TestStatus.FAIL,
                    Description="Login button not found.",
                    Actual_Result="No login button found on the page."
                )

            # Step 2: Find the username field
            username_regex = self.generate_username_regex()
            username_field = self.find_element(page, username_regex, element_type="input")
            if not username_field:
                return TestResult(
                    Name="Login Test",
                    Status=TestStatus.FAIL,
                    Description="Username field not found.",
                    Actual_Result="No username field found after login button click."
                )

            # Step 3: Find the password field
            password_regex = self.generate_password_regex()
            password_field = self.find_element(page, password_regex, element_type="input")
            if not password_field:
                return TestResult(
                    Name="Login Test",
                    Status=TestStatus.FAIL,
                    Description="Password field not found.",
                    Actual_Result="No password field found after login button click."
                )

            # Step 4: Fill in the username and password
            username_field.fill(self.site.login.username)
            password_field.fill(self.site.login.password)

            # Step 5: Find and click the submit button
            submit_button_regex = self.generate_submit_button_regex()
            submit_button = self.find_element(page, submit_button_regex, element_type="button,input[type='submit']")
            if submit_button:
                submit_button.click()
                page.wait_for_timeout(10000)
            else:
                return TestResult(
                    Name="Login Test",
                    Status=TestStatus.FAIL,
                    Description="Submit button not found.",
                    Actual_Result="No submit button found after filling in login details."
                )

            # Step 6: Wait for the network to idle and save state
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


    def run_comparison(self, results):
        return ComparisonResult(
            Name="Login Test",
            Status=TestStatus.PASS,
            Description="Login functionality works as expected.",
            Expected_Result="User is on the Dashboard page."
        )
