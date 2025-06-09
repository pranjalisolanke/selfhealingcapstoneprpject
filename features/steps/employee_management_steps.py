# features/steps/employee_management_steps.py
from behave import given, when, then
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.pim_page import PIMPage
import os
import logging


@when('I navigate to the PIM module')
def step_navigate_to_pim(context):
    logging.info("Navigating to PIM module")
    # Use the dashboard_page that was created during login
    context.dashboard_page.navigate_to_pim()
    
    # Store PIM page for later steps
    context.pim_page = PIMPage(context.driver)
    logging.info("PIM module loaded")

@when('I click on "Add Employee"')
def step_click_add_employee(context):
    logging.info("Clicking Add Employee button")
    context.pim_page.click_add_employee()
    logging.info("Add Employee form loaded")

@when('I enter employee details')
def step_enter_employee_details(context):
    logging.info("Entering employee details")
    # Get the first row of data (excluding header)
    row = context.table[0]
    first_name = row['First Name']
    last_name = row['Last Name']
    middle_name = row['Middle Name']
    employee_id = row['Employee ID']
    
    # Store for later verification
    context.employee_full_name = f"{first_name} {last_name} {middle_name} {employee_id }"
    
    # Enter the details
    context.pim_page.enter_employee_details(first_name, last_name, middle_name, employee_id)
    logging.info(f"Entered details for employee: {first_name} {last_name}{middle_name}  ID: {employee_id}") 


@when('I click Save')
def step_click_save(context):
    logging.info("Clicking Save button")
    context.pim_page.click_save()
    logging.info("Save operation completed")

@then('I should see a success message')
def step_verify_success_message(context):
    logging.info("Checking for success message")
    assert context.pim_page.is_success_message_displayed(), "Success message not displayed"
    logging.info("Success message verified")

@then('the employee "{employee_name}" should be in the employee list')
def step_verify_employee_in_list(context, employee_name):
    logging.info(f"Verifying employee {employee_name} is in the list")
    # Navigate back to employee list if needed
    if not context.pim_page.is_element_visible(context.pim_page.employee_list_heading):
        logging.info("Navigating back to employee list")
        # Use the existing dashboard_page from context
        context.dashboard_page.navigate_to_pim()
    
    # Search for the employee
    logging.info(f"Searching for employee: {employee_name}")
    context.pim_page.search_employee(employee_name)
    
    # Verify employee is in the list
    assert context.pim_page.is_employee_in_list(employee_name), f"Employee '{employee_name}' not found in the list"
    logging.info(f"Employee {employee_name} found in the list")
