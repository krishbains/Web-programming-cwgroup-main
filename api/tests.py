#Testing was done in FIrefox, using geckodriver
from django.test import TestCase
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class SignupTest(LiveServerTestCase):
    def setUp(self):
        # Start Firefox WebDriver
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)  # Wait for elements to load

    def tearDown(self):
        # Quit the WebDriver after each test
        self.driver.quit()

    def test_signup(self):
        # Navigate to the signup page
        self.driver.get(self.live_server_url + "/register/")
        
        # Fill in the signup form
        self.driver.find_element(By.NAME, "username").send_keys("seleniumtestuser")
        self.driver.find_element(By.NAME, "email").send_keys("seleniumtestuser@example.com")
        self.driver.find_element(By.NAME, "password1").send_keys("seleniumpassword123")
        self.driver.find_element(By.NAME, "password2").send_keys("seleniumpassword123")
        self.driver.find_element(By.NAME, "date_of_birth").send_keys("2000-01-01")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Assert successful signup
        self.assertIn("Welcome", self.driver.page_source)  # Adjust based on the redirect
