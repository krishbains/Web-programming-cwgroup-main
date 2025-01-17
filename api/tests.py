from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options


class SignupTest(LiveServerTestCase):
    def setUp(self):
        # Configure Firefox options
        firefox_options = Options()
        # Running with browser visible - no headless mode
        firefox_options.add_argument('--no-sandbox')
        firefox_options.add_argument('--disable-dev-shm-usage')

        # Start Firefox WebDriver with options
        self.driver = webdriver.Firefox(options=firefox_options)
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 15)

    def tearDown(self):
        # Quit the WebDriver after each test
        self.driver.quit()

    def test_signup(self):
        try:
            # Navigate to the signup page
            self.driver.get(f"{self.live_server_url}/register/")

            # Wait for form to be present
            form = self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "form"))
            )

            # Fill in the signup form
            form.find_element(By.NAME, "username").send_keys("seleniumtestuser")
            form.find_element(By.NAME, "email").send_keys("seleniumtestuser@example.com")
            form.find_element(By.NAME, "password1").send_keys("seleniumpassword123")
            form.find_element(By.NAME, "password2").send_keys("seleniumpassword123")
            form.find_element(By.NAME, "date_of_birth").send_keys("2000-01-01")

            # Submit the form
            submit_button = form.find_element(By.CSS_SELECTOR, "button[type='submit']")
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
            submit_button.click()

            # Wait for the greeting
            greeting = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Hello,')]"))
            )

            # Assert the greeting
            self.assertIn("Hello,", greeting.text)

        except TimeoutException as e:
            # Enhanced error reporting
            print("\nTest failed with TimeoutException:")
            print(f"Current URL: {self.driver.current_url}")
            print("\nPage source:")
            print(self.driver.page_source)
            raise e