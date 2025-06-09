# pages/login_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time
from selenium.webdriver.support.ui import WebDriverWait

class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        
        # Define locators with intentionally wrong strategies to demonstrate AI healing
        self.username_field = self.create_ai_locator(
            "username_field",
            "username input field on login page",
            (By.NAME, 'username'),  # AI-learned primary locator
        )
        
        self.password_field = self.create_ai_locator(
            "password_field",
            "password input field on login page",
            (By.NAME, 'password'),  # AI-learned primary locator
        )
        
        self.login_button = self.create_ai_locator(
            "login_button",
            "login submit button",
            (By.CSS_SELECTOR, "button[type='submit']"),  # AI-learned primary locator
        )
        
        self.login_form = self.create_ai_locator(
            "login_form",
            "login form container",
            (By.CSS_SELECTOR, "form.wrong-login-form")  # Wrong locator
        )
        
        self.logo = self.create_ai_locator(
            "logo",
            "OrangeHRM logo on login page",
            (By.CSS_SELECTOR, "img.wrong-logo")  # Wrong locator
        )
    
    def navigate_to(self, url):
        """Navigate to the login page"""
        self.driver.driver.get(url)
        self.wait_for_page_load()
    
    def wait_for_page_load(self, timeout=10):
        """Wait for page to load completely"""
        try:
            WebDriverWait(self.driver.driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            # Add a small delay to allow any JavaScript to finish
            time.sleep(0.5)
        except Exception as e:
            print(f"⚠️ Page did not load completely after {timeout} seconds: {str(e)}")
    
    def enter_username(self, username):
        """Enter username in the username field"""
        self.input_text(self.username_field, username)
    
    def enter_password(self, password):
        """Enter password in the password field"""
        self.input_text(self.password_field, password)
    
    def click_login_button(self):
        """Click the login button"""
        self.click(self.login_button)
        self.wait_for_page_load()
    
    def login(self, username, password):
        """Login with the given credentials"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
    
    def is_login_page_loaded(self):
        """Check if login page is loaded correctly"""
        return self.is_element_visible(self.login_form) and self.is_element_visible(self.logo)
