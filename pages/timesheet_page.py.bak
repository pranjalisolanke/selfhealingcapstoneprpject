# pages/timesheet_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import os
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging

class TimesheetPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        
        # All locators with self-healing capability
        self.time_menu = self.create_ai_locator(
            "time_menu",
            "Time menu item in the main navigation",
            (By.XPATH, "//span[text()='Time']"), 
        )
        
        self.employee_name_input = self.create_ai_locator(
            "employee_name_input",
            "Employee name input field on timesheet page",
            (By.XPATH, "//input[@placeholder='Type for hints...']"),  # Primary locator
        )
        
        self.employee_autocomplete_option = self.create_ai_locator(
            "employee_autocomplete_option",
            "Autocomplete option for employee name",
            (By.XPATH, "//div[@role='option']"),  # Primary locator
        )
        
        self.view_button = self.create_ai_locator(
            "view_button",
            "View button on timesheet page",
            (By.XPATH, "//button[@type='submit']"),  # Primary locator
        )
        
        self.timesheet_status = self.create_ai_locator(
            "timesheet_status",
            "Timesheet status indicator",
            (By.XPATH, "//*[contains(@class, 'timesheet')]"),  # AI-learned primary locator
        )
        
        self.timesheet_table = self.create_ai_locator(
            "timesheet_table",
            "Timesheet data table",
            (By.XPATH, "//*[contains(@class, 'timesheet')]"),  # AI-learned primary locator
        )
        
        self.timesheet_hours = self.create_ai_locator(
            "timesheet_hours",
            "Hours recorded in timesheet",
            (By.XPATH, "//div[contains(@class,'oxd-table-cell')]//div[contains(@class,'oxd-table-cell-actions')]"),  # Primary locator
        )
        
        self.add_timesheet_button = self.create_ai_locator(
            "add_timesheet_button",
            "Add timesheet button",
            (By.XPATH, "//button[contains(.,'Add')]"),  # Primary locator
        )
        
        self.edit_button = self.create_ai_locator(
            "edit_button",
            "Edit button for timesheet",
            (By.XPATH, "//button[contains(.,'Edit')]"),  # Primary locator
        )
        
        self.submit_button = self.create_ai_locator(
            "submit_button",
            "Submit button for timesheet",
            (By.XPATH, "//button[contains(.,'Submit')]"),  # Primary locator
        )
        
        self.confirm_button = self.create_ai_locator(
            "confirm_button",
            "Confirm button in dialog",
            (By.XPATH, "//div[contains(@class,'oxd-dialog-container')]//button[contains(.,'Yes')]"),  # Primary locator
        )
        
        self.success_message = self.create_ai_locator(
            "success_message",
            "Success message after timesheet operation",
            (By.XPATH, "//div[contains(@class,'oxd-toast-container')]"),  # Primary locator
        )
    
    def navigate_to_timesheet(self):
        logging.info("Navigating to Timesheet page")
        self.click(self.time_menu)
        self.wait_for_page_load()
        self.wait_for_element_visible(self.employee_name_input, timeout=15)
        logging.info("Timesheet page loaded successfully")
    
    def enter_employee_name(self, employee_name):
        logging.info(f"Entering employee name: {employee_name}")
        self.input_text(self.employee_name_input, employee_name)
        time.sleep(2)  # Wait for autocomplete
        
        try:
            self.click(self.employee_autocomplete_option)
            logging.info("Selected employee from autocomplete options")
        except Exception as e:
            logging.warning(f"⚠️ Could not select employee from autocomplete: {str(e)}")
    
    def click_view_button(self):
        logging.info("Clicking View button")
        self.click(self.view_button)
        self.wait_for_page_load()
        logging.info("View button clicked")
    
    def verify_timesheet_status(self):
        logging.info("Verifying timesheet status")
        status_element = self.wait_for_element_visible(self.timesheet_status, timeout=15)
        if status_element:
            status_text = self.get_text(self.timesheet_status)
            logging.info(f"Timesheet status: {status_text}")
            return status_text
        else:
            logging.warning("⚠️ Could not verify timesheet status")
            return None
    
    def verify_recorded_hours(self):
        logging.info("Verifying recorded hours in timesheet")
        if self.is_element_visible(self.timesheet_table):
            try:
                hours_elements = self.driver.find_elements(self.timesheet_hours)
                hours_count = len(hours_elements)
                logging.info(f"Found {hours_count} hour entries in timesheet")
                return hours_count > 0
            except Exception as e:
                logging.warning(f"⚠️ Error checking timesheet hours: {str(e)}")
                
                # Fallback verification - check if table has content
                table_html = self.get_element_html(self.timesheet_table)
                has_content = len(table_html.strip()) > 50  # Arbitrary length check
                logging.info(f"Fallback verification - table has content: {has_content}")
                return has_content
        else:
            logging.warning("⚠️ Timesheet table not visible")
            return False
    
    def wait_for_element_visible(self, locator, timeout=10):
        try:
            logging.info(f"Waiting for element {locator.name} to be visible")
            element = self.driver.find_element(locator)
            WebDriverWait(self.driver.driver, timeout).until(
                EC.visibility_of(element)
            )
            logging.info(f"Element {locator.name} is now visible")
            return element
        except TimeoutException:
            logging.warning(f"⚠️ Element {locator.name} not visible after {timeout} seconds")
            return None
    
    def wait_for_page_load(self, timeout=10):
        try:
            logging.info("Waiting for page to load completely")
            WebDriverWait(self.driver.driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            time.sleep(0.5)
            logging.info("Page loaded completely")
        except Exception as e:
            logging.warning(f"⚠️ Page did not load completely after {timeout} seconds: {str(e)}")
    
    def is_element_visible(self, locator, timeout=5):
        try:
            element = self.driver.find_element(locator)
            WebDriverWait(self.driver.driver, timeout).until(
                EC.visibility_of(element)
            )
            return True
        except (TimeoutException, Exception) as e:
            logging.warning(f"⚠️ Element {locator.name} not visible: {str(e)}")
            return False
    
    def get_element_html(self, locator):
        element = self.driver.find_element(locator)
        return element.get_attribute("outerHTML")
    
    def get_text(self, locator):
        element = self.driver.find_element(locator)
        return element.text
    
    def update_source_code_with_learned_locators(self):
        from utils.code_updater import update_source_code_with_locators
        if hasattr(self.driver, 'learned_locators'):
            update_source_code_with_locators("pages/timesheet_page.py", self.driver.learned_locators)
