# pages/leave_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LeavePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        
        # Define locators with intentionally wrong strategies
        self.apply_leave_menu = self.create_ai_locator(
            "apply_leave_menu",
            "Apply leave menu item",
            (By.XPATH, "//a[contains(text(), 'Wrong Apply')]")  # Wrong locator
        )
        
        self.my_leave_menu = self.create_ai_locator(
            "my_leave_menu",
            "My Leave menu item",
            (By.XPATH, "//a[contains(text(), 'Wrong My Leave')]")  # Wrong locator
        )
        
        self.leave_type_dropdown = self.create_ai_locator(
            "leave_type_dropdown",
            "Leave type dropdown",
            (By.CSS_SELECTOR, "div.wrong-dropdown")  # Wrong locator
        )
        
        self.from_date_input = self.create_ai_locator(
            "from_date_input",
            "From date input field",
            (By.NAME, "wrong_fromDate")  # Wrong locator
        )
        
        self.to_date_input = self.create_ai_locator(
            "to_date_input",
            "To date input field",
            (By.NAME, "wrong_toDate")  # Wrong locator
        )
        
        self.comments_textarea = self.create_ai_locator(
            "comments_textarea",
            "Comments textarea",
            (By.NAME, "wrong_comments")  # Wrong locator
        )
        
        self.apply_button = self.create_ai_locator(
            "apply_button",
            "Apply button on leave form",
            (By.XPATH, "//button[text()='Wrong Apply']")  # Wrong locator
        )
        
        self.leave_list_table = self.create_ai_locator(
            "leave_list_table",
            "Leave list table",
            (By.CSS_SELECTOR, "table.wrong-table")  # Wrong locator
        )
        
        self.leave_status_cell = self.create_ai_locator(
            "leave_status_cell",
            "Leave status cell in the table",
            (By.CSS_SELECTOR, "td.wrong-status")  # Wrong locator
        )
    
    def click_apply(self):
        """Click on Apply menu item"""
        self.click(self.apply_leave_menu)
        self.wait_for_page_load()
    
    def navigate_to_my_leave(self):
        """Navigate to My Leave page"""
        self.click(self.my_leave_menu)
        self.wait_for_page_load()
    
    def select_leave_type(self, leave_type):
        """Select leave type from dropdown"""
        self.click(self.leave_type_dropdown)
        self.wait_for_page_load()
        
        # Find and click the option with the given text
        option_locator = self.create_ai_locator(
            "leave_type_option",
            f"Leave type option for {leave_type}",
            (By.XPATH, f"//div[contains(text(), '{leave_type}')]")
        )
        self.click(option_locator)
    
    def set_from_date(self, date):
        """Set the from date"""
        self.clear_and_input_text(self.from_date_input, date)
        # Click outside to close any date picker
        self.click_body()
    
    def set_to_date(self, date):
        """Set the to date"""
        self.clear_and_input_text(self.to_date_input, date)
        # Click outside to close any date picker
        self.click_body()
    
    def enter_comments(self, comments):
        """Enter comments"""
        self.input_text(self.comments_textarea, comments)
    
