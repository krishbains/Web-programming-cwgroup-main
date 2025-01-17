from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import time


class ProfileTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print(f"\nLive Server URL: {cls.live_server_url}")

    def setUp(self):
        firefox_options = Options()
        firefox_options.add_argument('--no-sandbox')
        firefox_options.add_argument('--disable-dev-shm-usage')
        firefox_options.add_argument('--window-size=1920,1080')

        self.driver = webdriver.Firefox(options=firefox_options)
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 15)
        print("\nSetup completed, browser initialized")

    def tearDown(self):
        if hasattr(self, 'driver'):
            # Capture page source if test failed
            if hasattr(self._outcome, 'errors'):
                for test, exc_info in self._outcome.errors:
                    if exc_info:
                        print("\nTest failed! Current page source:")
                        print(self.driver.page_source)
                        break
            self.driver.quit()

    def register_user(self):
        try:
            print("\nStarting user registration")
            self.driver.get(f"{self.live_server_url}/register/")
            print(f"Navigated to register page: {self.driver.current_url}")

            # Wait for and verify form presence
            form = self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "form"))
            )
            print("Registration form found")

            # Fill form fields
            fields = {
                "username": "testuser",
                "email": "testuser@example.com",
                "password1": "testpassword123",
                "password2": "testpassword123",
                "date_of_birth": "2000-01-01"
            }

            for name, value in fields.items():
                try:
                    field = form.find_element(By.NAME, name)
                    field.clear()
                    field.send_keys(value)
                    print(f"Filled {name} field")
                except Exception as e:
                    print(f"Error filling {name} field: {str(e)}")
                    raise

            # Submit form
            print("Submitting registration form")
            submit_button = form.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_button.click()

            # Wait for navigation
            time.sleep(2)
            print(f"After registration, current URL: {self.driver.current_url}")

            # Verify successful registration
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "nav.navigation"))
            )
            print("Navigation menu found - registration successful")

            return True

        except Exception as e:
            print(f"\nRegistration failed with error: {str(e)}")
            print(f"Current URL: {self.driver.current_url}")
            print("Page source:")
            print(self.driver.page_source)
            raise

    def test_profile_page(self):
        try:
            print("\nStarting profile page test")
            self.register_user()

            print("\nNavigating to profile page")
            self.driver.get(f"{self.live_server_url}/profile/")
            print(f"Current URL after navigation: {self.driver.current_url}")

            # Give Vue time to render
            time.sleep(2)

            # Check for profile elements
            profile_container = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "profile-container"))
            )
            print("Profile container found")

            # Verify username
            username_element = profile_container.find_element(
                By.XPATH, "//div[contains(@class, 'detail-item')]/strong[contains(text(), 'Username:')]/.."
            )
            print(f"Found username element: {username_element.text}")
            self.assertIn("testuser", username_element.text)

            # Find edit button
            edit_button = profile_container.find_element(By.CLASS_NAME, "edit-btn")
            print("Found edit button")

            print("\nProfile page test completed successfully")

        except Exception as e:
            print(f"\nProfile page test failed with error: {str(e)}")
            print(f"Current URL: {self.driver.current_url}")
            print("Page source at time of error:")
            print(self.driver.page_source)
            raise

        def test_profile_edit(self):
            try:
                print("\nStarting profile edit test")
                # First register and get to profile page
                self.register_user()

                print("\nNavigating to profile page")
                self.driver.get(f"{self.live_server_url}/profile/")
                time.sleep(2)  # Wait for Vue to render

                # Click edit button
                edit_button = self.wait.until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "edit-btn"))
                )
                edit_button.click()
                print("Clicked edit button")

                # Wait for edit form
                form = self.wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, "edit-form"))
                )
                print("Found edit form")

                # Update profile information
                new_data = {
                    "username": "updated_user",
                    "email": "updated@example.com",
                    "date_of_birth": "1995-12-25",
                    "current_password": "testpassword123",  # Original password from registration
                    "new_password": "newpassword456"
                }

                # Fill in each field
                for field_id, value in new_data.items():
                    try:
                        field = form.find_element(By.ID, field_id)
                        field.clear()
                        field.send_keys(value)
                        print(f"Updated {field_id} field")
                    except Exception as e:
                        print(f"Error updating {field_id}: {str(e)}")
                        raise

                # Submit form
                save_button = form.find_element(By.CLASS_NAME, "save-btn")
                save_button.click()
                print("Clicked save button")

                # Wait for profile details to reappear
                profile_details = self.wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, "profile-details"))
                )
                print("Profile details reappeared")

                # Verify updates
                time.sleep(2)  # Wait for data to refresh
                detail_items = profile_details.find_elements(By.CLASS_NAME, "detail-item")

                for item in detail_items:
                    text = item.text
                    if "Username:" in text:
                        self.assertIn("updated_user", text)
                        print("Username verified")
                    elif "Email:" in text:
                        self.assertIn("updated@example.com", text)
                        print("Email verified")
                    elif "Date of Birth:" in text:
                        self.assertIn("12/25/1995", text)
                        print("Date of birth verified")

                print("\nProfile edit test completed successfully")

                # Test logging in with new password
                print("\nTesting login with new password")
                self.driver.get(f"{self.live_server_url}/logout/")
                time.sleep(1)
                self.driver.get(f"{self.live_server_url}/login/")

                login_form = self.wait.until(
                    EC.presence_of_element_located((By.TAG_NAME, "form"))
                )

                # Login with new credentials
                login_form.find_element(By.NAME, "username").send_keys("updated_user")
                login_form.find_element(By.NAME, "password").send_keys("newpassword456")
                login_form.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

                # Verify successful login
                self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "nav.navigation"))
                )
                print("Successfully logged in with new credentials")

            except Exception as e:
                print(f"\nProfile edit test failed with error: {str(e)}")
                print(f"Current URL: {self.driver.current_url}")
                print("Page source at time of error:")
                print(self.driver.page_source)
                raise

