# pages/dashboard_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class DashboardPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        
        # Define locators with intentionally wrong strategies to demonstrate AI healing
        self.user_dropdown = self.create_ai_locator(
            "user_dropdown",
            "User dropdown menu in the top right corner with the user's name",
            (By.CSS_SELECTOR, ".wrong-user-dropdown")  # Wrong locator
        )
        
        # Dashboard elements
        self.dashboard_heading = self.create_ai_locator(
            "dashboard_heading",
            "Dashboard heading or title on the main dashboard page",
            (By.CSS_SELECTOR, "h6.wrong-dashboard-heading")  # Wrong locator
        )
        
        self.quick_launch_panel = self.create_ai_locator(
            "quick_launch_panel",
            "Quick Launch panel on dashboard with shortcut icons",
            (By.CSS_SELECTOR, ".wrong-quick-launch")  # Wrong locator
        )
        
        # Main menu items
        self.admin_menu_item = self.create_ai_locator(
            "admin_menu_item",
            "Admin module menu item in the left sidebar navigation",
            (By.XPATH, "//span[text()='Wrong Admin Text']")  # Wrong locator
        )
        
        self.pim_menu_item = self.create_ai_locator(
            "pim_menu_item",
            "PIM module menu item in the left sidebar navigation",
            (By.XPATH, "//span[text()='PIM']")  # Wrong locator
        )
        
        self.leave_menu_item = self.create_ai_locator(
            "leave_menu_item",
            "Leave module menu item in the left sidebar navigation",
            (By.XPATH, "//span[text()='Wrong Leave Text']")  # Wrong locator
        )
    
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
    
    def is_element_visible(self, locator, timeout=5):
        """Check if an element is visible"""
        try:
            element = self.driver.find_element(locator)
            WebDriverWait(self.driver.driver, timeout).until(
                EC.visibility_of(element)
            )
            return True
        except (TimeoutException, Exception) as e:
            print(f"⚠️ Element {locator.name} not visible: {str(e)}")
            return False
    
    def is_dashboard_loaded(self):
        """Check if dashboard is loaded"""
        return self.is_element_visible(self.dashboard_heading)
    
    def navigate_to_admin(self):
        """Navigate to the Admin module"""
        self.click(self.admin_menu_item)
        self.wait_for_page_load()
    
    def navigate_to_pim(self):
        """Navigate to the PIM module"""
        self.click(self.pim_menu_item)
        self.wait_for_page_load()
    
    def navigate_to_leave(self):
        """Navigate to the Leave module"""
        self.click(self.leave_menu_item)
        self.wait_for_page_load()
    
    def logout(self):
        """Logout from the application"""
        self.click(self.user_dropdown)
        
        # Find and click the logout link
        logout_link = self.create_ai_locator(
            "logout_link",
            "Logout link in user dropdown menu",
            (By.XPATH, "//a[contains(text(), 'Wrong Logout')]")  # Wrong locator
        )
        self.click(logout_link)
        self.wait_for_page_load()
