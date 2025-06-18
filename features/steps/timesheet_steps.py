from behave import given, when, then
from pages.login_page import LoginPage
from pages.timesheet_page import TimesheetPage
import logging
import time

@when('I navigate to time module')
def step_navigate_to_timesheet(context):
    logging.info("Navigating to timesheet page")
    context.timesheet_page = TimesheetPage(context.driver)
    context.timesheet_page.navigate_to_timesheet()
    logging.info("Navigated to timesheet page")

@when('I enter text in employee name textbox')
def step_enter_employee_name(context):
    logging.info("Entering employee name")
    context.timesheet_page.enter_employee_name("1Sam Anderson 2 2")
    logging.info("Employee name entered")

@when('I click on the view button')
def step_click_view_button(context):
    logging.info("Clicking view button")
    context.timesheet_page.click_view_button()
    time.sleep(2)
    logging.info("View button clicked")

@then('I verify the timesheet status')
def step_verify_timesheet_status(context):
    logging.info("Verifying timesheet status")
    status_text = context.timesheet_page.verify_timesheet_status()
    assert status_text is not None, "Timesheet status could not be verified"
    logging.info(f"Timesheet status verified: {status_text}")
    if hasattr(context.driver, 'learned_locators') and context.driver.learned_locators:
        logging.info("Updating source code with learned locators")
        context.timesheet_page.update_source_code_with_learned_locators()

@then('my timesheet should show the recorded hours')
def step_verify_recorded_hours(context):
    logging.info("Verifying recorded hours in timesheet")
    has_hours = context.timesheet_page.verify_recorded_hours()
    assert has_hours, "No hours were found in the timesheet"
    logging.info("Successfully verified timesheet has recorded hours")

    screenshot_path = f"screenshots/timesheet_hours_{time.strftime('%Y%m%d_%H%M%S')}.png"
    context.driver.save_screenshot(screenshot_path)
    logging.info(f"Screenshot saved to {screenshot_path}")
    
    if hasattr(context.driver, 'learned_locators') and context.driver.learned_locators:
        logging.info("Updating source code with learned locators")
        context.timesheet_page.update_source_code_with_learned_locators()