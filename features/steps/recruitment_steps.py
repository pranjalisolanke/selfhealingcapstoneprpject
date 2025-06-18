from behave import when, then
from pages.recruitment_page import RecruitmentPage
import logging
import time

@when('I navigate to recruitment module')
def step_navigate_to_recruitment(context):
    logging.info("Navigating to recruitment module")
    context.recruitment_page = RecruitmentPage(context.driver)
    context.recruitment_page.navigate_to_recruitment()
    logging.info("Navigated to recruitment module")

@when('I click on the add button')
def step_click_add_button(context):
    logging.info("Clicking add button")
    context.recruitment_page.click_add_button()
    logging.info("Add button clicked")

@when('I enter candidate details')
def step_enter_candidate_details(context):
    logging.info("Entering candidate details")
    row = context.table[0]
    first_name = row['First Name']
    middle_name = row['Middle Name']
    last_name = row['Last Name']
    email = row['Email']
    vacancy = row['Vacancy']

    context.candidate_full_name = f"{first_name} {middle_name} {last_name}"
    context.recruitment_page.enter_candidate_details(
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        email=email,
        vacancy=vacancy
    )
    logging.info("Candidate details entered")

@when('I click on the save button')
def step_click_save_button(context):
    logging.info("Clicking save button")
    context.recruitment_page.click_save_button()
    logging.info("Save button clicked")

@then('I should see a success toast message')
def step_verify_success_message(context):
    logging.info("Verifying success message")
    assert context.recruitment_page.is_success_message_displayed(), "Success message not displayed"
    logging.info("Success message verified")
    
    if hasattr(context.driver, 'learned_locators') and context.driver.learned_locators:
        logging.info("Updating source code with learned locators")
        context.recruitment_page.update_source_code_with_learned_locators()

@then('the candidate should be added to the list')
def step_verify_candidate_added(context):
    logging.info("Verifying candidate was added to the list")
    time.sleep(2)
    assert context.recruitment_page.is_candidate_in_list(context.candidate_full_name), \
        f"Candidate {context.candidate_full_name} not found in the list"
    logging.info("Candidate verified in the list")

    if hasattr(context.driver, 'learned_locators') and context.driver.learned_locators:
        logging.info("Updating source code with learned locators")
        context.recruitment_page.update_source_code_with_learned_locators()