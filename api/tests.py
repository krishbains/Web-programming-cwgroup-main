#Testing was done in Firefox, using geckodriver
from django.test import TestCase
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class SignupTest(LiveServerTestCase):
    def setUp(self):
        # Start Firefox WebDriver
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)  # Implicit wait for elements
        self.wait = WebDriverWait(self.driver, 15)  # Explicit wait for dynamic elements

    def tearDown(self):
        # Quit the WebDriver after each test
        self.driver.quit()

    def test_signup(self):
        try:
            # Navigate to the signup page
            self.driver.get(self.live_server_url + "/register/")
            
            # Fill in the signup form
            self.driver.find_element(By.NAME, "username").send_keys("seleniumtestuser")
            self.driver.find_element(By.NAME, "email").send_keys("seleniumtestuser@example.com")
            self.driver.find_element(By.NAME, "password1").send_keys("seleniumpassword123")
            self.driver.find_element(By.NAME, "password2").send_keys("seleniumpassword123")
            self.driver.find_element(By.NAME, "date_of_birth").send_keys("2000-01-01")
            self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

            # Wait for the dynamic greeting to appear
            greeting = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Hello,')]"))
            )

            # Assert the greeting is correct
            self.assertIn("Hello,", greeting.text)
        except TimeoutException:
            print(self.driver.page_source)  # Debug the page source if the test fails
            self.fail("Signup test failed due to timeout.")
