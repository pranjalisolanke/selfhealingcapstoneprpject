# pages/pim_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import os
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging

class PIMPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        
        # Define locators with intentionally wrong strategies to trigger self-healing
        self.add_employee_button = self.create_ai_locator(
            "add_employee_button",
            "Add Employee button on PIM page",
            (By.XPATH, "//header//nav//li//a[contains(text(),'Add Employee')]")  # Wrong locator
        )
        self.employee_list_heading = self.create_ai_locator(
            "employee_list_heading",
            "Employee List heading on PIM page",
            (By.CSS_SELECTOR, "h5.wrong-heading")  # Wrong locator
        )
        self.first_name_field = self.create_ai_locator(
            "first_name_field",
            "First name input field on Add Employee page",
            (By.NAME, "wrong_firstName")  # Wrong locator
        )
        self.middle_name_input = self.create_ai_locator(
            "middle_name_input",
            "Middle name input field on Add Employee page",
            (By.NAME, "wrong_middleName"),
        )
        self.last_name_field = self.create_ai_locator(
            "last_name_field",
            "Last name input field on Add Employee page",
            (By.NAME, "wrong_lastName")  # Wrong locator
        )
        self.employee_id_field = self.create_ai_locator(
            "employee_id_field",
            "Employee ID input field on Add Employee page",
            (By.XPATH, "//input[contains(@class, 'oxd-input') and contains(@class, 'oxd-input--focus')]")  # Wrong locator
        )
        self.save_button = self.create_ai_locator(
            "save_button",
            "Save button on Add Employee page",
            (By.XPATH, "//button[@type='submit']")  # Wrong locator
        )
        self.success_message = self.create_ai_locator(
            "success_message",
            "Success message after adding employee",
            (By.CSS_SELECTOR, ".wrong-success-message")  # Wrong locator
        )
        self.search_button = self.create_ai_locator(
            "search_button",
            "Search button on employee list",
            (By.CSS_SELECTOR, "button.wrong-search")  # Wrong locator
        )
        self.employee_name_search = self.create_ai_locator(
            "employee_name_search",
            "Employee name search input field",
            (By.CSS_SELECTOR, "input.wrong-employee-name")  # Wrong locator
        )
        self.employee_table = self.create_ai_locator(
            "employee_table",
            "Employee list table",
            (By.CSS_SELECTOR, "table.wrong-table")  # Wrong locator
        )
    
    def click_add_employee(self):
        logging.info("Attempting to click Add Employee button")
        self.click(self.add_employee_button)
        self.wait_for_page_load()
        self.wait_for_element_visible(self.first_name_field, timeout=15)
        logging.info("Add Employee form loaded")
    
    def enter_employee_details(self, first_name, last_name, middle_name, employee_id):
        logging.info(f"Entering employee details: {first_name} {middle_name} {last_name} ID: {employee_id}")
        self.input_text(self.first_name_field, first_name)
        self.input_text(self.middle_name_input, middle_name)
        self.input_text(self.last_name_field, last_name)
        self.clear_and_input_text(self.employee_id_field, employee_id)
        logging.info("Employee details entered")
    
    def upload_photo(self, file_path):
        logging.info(f"Uploading photo from: {file_path}")
        abs_file_path = os.path.abspath(file_path)
        self.input_file(self.photo_upload_button, abs_file_path)
        logging.info("Photo uploaded")
    
    def click_save(self):
        logging.info("Clicking Save button")
        self.click(self.save_button)
        self.wait_for_page_load()
        try:
            self.wait_for_element_visible(self.success_message, timeout=20)
            logging.info("Save operation completed successfully")
        except:
            logging.warning("Could not verify success message after save")
    
    def is_success_message_displayed(self):
        result = self.is_element_visible(self.success_message)
        logging.info(f"Success message displayed: {result}")
        return result
    
    def search_employee(self, employee_name):
        logging.info(f"Searching for employee: {employee_name}")
        self.input_text(self.employee_name_search, employee_name)
        self.click(self.search_button)
        self.wait_for_element_visible(self.employee_table, timeout=15)
        logging.info("Search completed")
    
    def is_employee_in_list(self, employee_name):
        logging.info(f"Checking if {employee_name} is in the employee list")
        table_html = self.get_element_html(self.employee_table)
        result = employee_name in table_html
        logging.info(f"Employee found in list: {result}")
        return result
    
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
    
    def input_file(self, locator, file_path):
        element = self.driver.find_element(locator)
        element.send_keys(file_path)

    # --- Optional: Update source code with learned locators for this page ---
    def update_source_code_with_learned_locators(self):
        from utils.code_updater import update_source_code_with_locators
        if hasattr(self.driver, 'learned_locators'):
            update_source_code_with_locators("pages/pim_page.py", self.driver.learned_locators)
