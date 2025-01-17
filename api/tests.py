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

    def test_account_creation_and_login(self):
        try:
            print("\nStarting account creation and login test")

            self.driver.get(f"{self.live_server_url}/register/")
            print("Navigated to register page")

            form = self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "form"))
            )

            test_data = {
                "username": "testuser123",
                "email": "testuser123@example.com",
                "password1": "securepassword123",
                "password2": "securepassword123",
                "date_of_birth": "2000-01-01"
            }

            for field_name, value in test_data.items():
                field = form.find_element(By.NAME, field_name)
                field.clear()
                field.send_keys(value)
                print(f"Filled {field_name} field")
                time.sleep(0.3)

            submit_button = form.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_button.click()
            print("Submitted registration form")

            nav = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "nav.navigation"))
            )
            print("Registration successful")

            # Logout
            logout_link = nav.find_element(By.CLASS_NAME, "logout-link")
            logout_link.click()
            print("Logged out successfully")

            time.sleep(2)

            login_form = self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "form"))
            )

            username_field = login_form.find_element(By.NAME, "username")
            password_field = login_form.find_element(By.NAME, "password")

            username_field.send_keys(test_data["username"])
            password_field.send_keys(test_data["password1"])

            login_form.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
            print("Submitted login form")

            nav = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "nav.navigation"))
            )

            profile_link = nav.find_element(By.XPATH, "//a[contains(@href, '/profile/')]")
            self.assertIsNotNone(profile_link)
            print("Login successful")

            profile_link.click()

            profile_details = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "profile-details"))
            )

            self.assertIn(test_data["username"], profile_details.text)
            self.assertIn(test_data["email"], profile_details.text)
            print("Profile information verified")

            print("Account creation and login test completed successfully")

        except Exception as e:
            print(f"\nTest failed with error: {str(e)}")
            print(f"Current URL: {self.driver.current_url}")
            print("Page source at time of error:")
            print(self.driver.page_source)
            raise

    def test_profile_edit(self):
        try:
            print("\nStarting profile edit test")
            self.register_user()

            print("\nNavigating to profile page")
            self.driver.get(f"{self.live_server_url}/profile/")
            time.sleep(2)

            edit_button = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "edit-btn"))
            )
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            self.driver.execute_script("arguments[0].click();", edit_button)
            print("Clicked Edit Profile button")
            time.sleep(1)

            form = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "edit-form"))
            )
            print("Found edit form")

            try:
                date_field = form.find_element(By.ID, "date_of_birth")
                self.driver.execute_script("arguments[0].scrollIntoView();", date_field)

                date_field.clear()
                date_field.send_keys("1995-12-25")

                date_value = date_field.get_attribute('value')
                print(f"Date field value after setting: {date_value}")
                assert date_value == "1995-12-25", "Date was not set correctly"

            except Exception as e:
                print(f"Error with date field: {str(e)}")
                raise

            fields_to_update = {
                "username": "updated_user",
                "email": "updated@example.com",
                "current_password": "testpassword123",
                "new_password": "newpassword456"
            }

            for field_id, value in fields_to_update.items():
                field = form.find_element(By.ID, field_id)
                field.clear()
                field.send_keys(value)
                print(f"Updated {field_id} field")
                time.sleep(0.3)

            save_button = form.find_element(By.CSS_SELECTOR, "button[type='submit']")
            self.driver.execute_script("arguments[0].scrollIntoView();", save_button)
            time.sleep(1)

            save_button.click()
            print("Clicked Save Changes button")

            try:
                alert = self.wait.until(EC.alert_is_present())
                print(f"Alert message: {alert.text}")
                alert.accept()
            except:
                print("No alert present")

            time.sleep(2)  # Wait for save to complete

            self.driver.refresh()
            time.sleep(2)

            detail_items = self.driver.find_elements(By.CLASS_NAME, "detail-item")
            for item in detail_items:
                text = item.text
                print(f"Checking detail item: {text}")

                if "Username:" in text:
                    self.assertIn("updated_user", text)
                    print("Username verified")
                elif "Email:" in text:
                    self.assertIn("updated@example.com", text)
                    print("Email verified")
                elif "Date of Birth:" in text:
                    self.assertIn("25/12/1995", text)  # Updated to match DD/MM/YYYY format
                    print("Date verified")

            print("\nProfile edit test completed successfully")

        except Exception as e:
            print(f"\nProfile edit test failed with error: {str(e)}")
            print(f"Current URL: {self.driver.current_url}")
            print("Page source:")
            print(self.driver.page_source)
            raise

    def test_user_search_and_friend_request_acceptance(self):
        try:
            print("\nStarting user search and friend request test with acceptance")

            self.register_user()

            from django.contrib.auth import get_user_model
            from datetime import date, timedelta

            User = get_user_model()

            today = date.today()
            target_user_birth_date = date(today.year - 98, today.month, today.day)

            target_user = User.objects.create_user(
                username='user99',
                email='user99@example.com',
                password='password123',
                date_of_birth=target_user_birth_date
            )

            from api.models import Hobby
            hobby = Hobby.objects.create(name='reading')
            target_user.hobbies.add(hobby)

            main_window = self.driver.current_window_handle

            print("\nNavigating to search page")
            self.driver.get(f"{self.live_server_url}/search/")
            time.sleep(2)

            min_age_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Min age']"))
            )
            max_age_input = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder='Max age']")

            min_age_input.clear()
            min_age_input.send_keys("98")
            time.sleep(0.5)

            max_age_input.clear()
            max_age_input.send_keys("98")
            time.sleep(0.5)

            filter_btn = self.driver.find_element(By.CLASS_NAME, "filter-btn")
            filter_btn.click()
            print("Applied age filters")

            time.sleep(2)

            user_cards = self.wait.until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "user-card"))
            )

            target_card = None
            for card in user_cards:
                if "user99" in card.text:
                    target_card = card
                    break

            self.assertIsNotNone(target_card, "Could not find the 98-year-old user")
            print("Found target user card")

            friend_request_btn = target_card.find_element(By.CLASS_NAME, "friend-request-btn")
            friend_request_btn.click()
            print("Sent friend request")

            self.driver.execute_script("window.open('');")
            new_window = [window for window in self.driver.window_handles if window != main_window][0]
            self.driver.switch_to.window(new_window)

            print("\nLogging in as target user")
            self.driver.get(f"{self.live_server_url}/login/")

            login_form = self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "form"))
            )

            username_field = login_form.find_element(By.NAME, "username")
            password_field = login_form.find_element(By.NAME, "password")

            username_field.send_keys("user99")
            password_field.send_keys("password123")
            login_form.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

            self.driver.get(f"{self.live_server_url}/friend-requests/")
            time.sleep(2)

            accept_btn = self.wait.until(
                EC.element_to_be_clickable((By.CLASS_NAME, "accept-btn"))
            )
            accept_btn.click()
            print("Clicked accept button")

            no_requests = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "no-requests"))
            )
            self.assertIn("No pending friend requests", no_requests.text)
            print("Successfully verified friend request acceptance")

        except Exception as e:
            print(f"\nTest failed with error: {str(e)}")
            print(f"Current URL: {self.driver.current_url}")
            print("Page source at time of error:")
            print(self.driver.page_source)
            raise
