from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import logging
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class RecruitmentPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        
        self.recruitment_menu = self.create_ai_locator(
            "recruitment_menu",
            "Recruitment menu item in the main navigation",
            (By.XPATH, "//span[text()='Recruitment']"),
        )
        
        self.add_button = self.create_ai_locator(
            "add_button",
            "Add button on recruitment page",
            (By.XPATH, "//button[normalize-space()='Add']"),
            [
                (By.CSS_SELECTOR, "button.oxd-button--secondary"),
                (By.XPATH, "//div[@class='orangehrm-header-container']/button")
            ]
        )
        
        self.first_name_input = self.create_ai_locator(
            "first_name_input",
            "First name input field on Add Candidate page",
            (By.XPATH, "//input[@name='firstName']"),
            [
                (By.XPATH, "//label[contains(text(),'First Name')]/following::input[1]"),
                (By.CSS_SELECTOR, "input[name='firstName']")
            ]
        )
        
        self.middle_name_input = self.create_ai_locator(
            "middle_name_input",
            "Middle name input field on Add Candidate page",
            (By.XPATH, "//input[@name='middleName']"),
            [
                (By.XPATH, "//label[contains(text(),'Middle Name')]/following::input[1]"),
                (By.CSS_SELECTOR, "input[name='middleName']")
            ]
        )
        
        self.last_name_input = self.create_ai_locator(
            "last_name_input",
            "Last name input field on Add Candidate page",
            (By.XPATH, "//input[@name='lastName']"),
            [
                (By.XPATH, "//label[contains(text(),'Last Name')]/following::input[1]"),
                (By.CSS_SELECTOR, "input[name='lastName']")
            ]
        )
        
        self.vacancy_dropdown = self.create_ai_locator(
            "vacancy_dropdown",
            "Vacancy dropdown on Add Candidate page",
            (By.XPATH, "//label[contains(text(),'Vacancy')]/following::div[contains(@class,'oxd-select-text')][1]"),
            [
                (By.XPATH, "//label[text()='Vacancy']/following::div[contains(@class,'oxd-select-wrapper')][1]"),
                (By.CSS_SELECTOR, "div.oxd-select-text")
            ]
        )
        
        self.email_input = self.create_ai_locator(
            "email_input",
            "Email input field on Add Candidate page",
            (By.XPATH, "//label[contains(text(),'Email')]/following::input[1]"),
            [
                (By.XPATH, "//label[text()='Email']/following::div[1]/input"),
                (By.CSS_SELECTOR, "input[placeholder='Type here']")
            ]
        )
        
        self.save_button = self.create_ai_locator(
            "save_button",
            "Save button on Add Candidate page",
            (By.XPATH, "//button[@type='submit']"),
            [
                (By.CSS_SELECTOR, "button[type='submit']"),
                (By.XPATH, "//button[contains(.,'Save')]")
            ]
        )
        
        self.success_message = self.create_ai_locator(
            "success_message",
            "Success message after adding candidate",
            (By.XPATH, "//div[contains(@class,'oxd-toast-container')]"),
            [
                (By.CSS_SELECTOR, "div.oxd-toast-container"),
                (By.XPATH, "//div[contains(@class,'oxd-toast')]")
            ]
        )
        
        self.candidate_list = self.create_ai_locator(
            "candidate_list",
            "Candidate list table",
            (By.XPATH, "//label[text()='Name']/parent::div/following-sibling::div//p[contains(@class,'oxd-text')]"),
            [
                (By.CSS_SELECTOR, "div.oxd-table-body"),
                (By.XPATH, "//div[@role='table']")
            ]
        )
    
    def navigate_to_recruitment(self):
        logging.info("Navigating to Recruitment page")
        self.click(self.recruitment_menu)
        self.wait_for_page_load()
        logging.info("Recruitment page loaded successfully")
    
    def click_add_button(self):
        logging.info("Clicking Add button")
        self.click(self.add_button)
        self.wait_for_page_load()
        self.wait_for_element_visible(self.first_name_input, timeout=15)
        logging.info("Add Candidate form loaded")
    
    def enter_candidate_details(self, first_name, middle_name, last_name, email, vacancy):
        logging.info(f"Entering candidate details: {first_name} {middle_name} {last_name}, {email}, {vacancy}")
        self.input_text(self.first_name_input, first_name)
        self.input_text(self.middle_name_input, middle_name)
        self.input_text(self.last_name_input, last_name)
        self.click(self.vacancy_dropdown)
        time.sleep(1)  
        vacancy_option = self.create_ai_locator(
            "vacancy_option",
            f"Vacancy option for {vacancy}",
            (By.XPATH, f"//div[@role='option']/span[contains(text(),'{vacancy}')]"),
            [
                (By.XPATH, f"//div[@role='listbox']//span[contains(text(),'{vacancy}')]"),
                (By.CSS_SELECTOR, f"div[role='option'] span")
            ]
        )
        self.click(vacancy_option)

        self.input_text(self.email_input, email)
        logging.info("Candidate details entered successfully")
    
    def click_save_button(self):
        logging.info("Clicking Save button")
        self.click(self.save_button)
        self.wait_for_page_load()
        logging.info("Save button clicked")
    
    def is_success_message_displayed(self):
        logging.info("Checking for success message")
        result = self.is_element_visible(self.success_message, timeout=10)
        if result:
            logging.info("Success message displayed")
        else:
            logging.warning("Success message not displayed")
        return result
    
    def is_candidate_in_list(self, candidate_name):
        logging.info(f"Checking if candidate {candidate_name} is in the list")
        self.wait_for_element_visible(self.candidate_list, timeout=15)
        candidate_list_html = self.get_element_html(self.candidate_list)
        result = candidate_name in candidate_list_html
        
        if result:
            logging.info(f"Candidate {candidate_name} found in the list")
        else:
            logging.warning(f"Candidate {candidate_name} not found in the list")
        
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
    
    def update_source_code_with_learned_locators(self):
        from utils.code_updater import update_source_code_with_locators
        if hasattr(self.driver, 'learned_locators'):
            update_source_code_with_locators("pages/recruitment_page.py", self.driver.learned_locators)