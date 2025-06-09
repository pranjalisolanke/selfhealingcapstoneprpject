# features/steps/leave_management_steps.py
from behave import given, when, then
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.leave_page import LeavePage

@given('I am logged in as an employee')
def step_login_as_employee(context):
    login_page = LoginPage(context.driver)
    login_page.navigate_to("https://opensource-demo.orangehrmlive.com/")
    login_page.login("Admin", "admin123")  # Using admin for demo, but could be any employee
    
    # Verify we're on the dashboard
    dashboard_page = DashboardPage(context.driver)
    assert dashboard_page.is_element_visible(dashboard_page.user_dropdown), "Login failed"

@when('I navigate to the Leave module')
def step_navigate_to_leave(context):
    dashboard_page = DashboardPage(context.driver)
    dashboard_page.navigate_to_leave()
    
    # Store Leave page for later steps
    context.leave_page = LeavePage(context.driver)

@when('I click on "Apply"')
def step_click_apply(context):
    context.leave_page.click_apply()

@when('I select leave details')
def step_select_leave_details(context):
    # Get the first row of data (excluding header)
    row = context.table[0]
    leave_type = row['Leave Type']
    from_date = row['From Date']
    to_date = row['To Date']
    comments = row['Comments']
    
    # Enter the details
    context.leave_page.select_leave_type(leave_type)
    context.leave_page.set_from_date(from_date)
    context.leave_page.set_to_date(to_date)
    context.leave_page.enter_comments(comments)

@when('I click Apply')
def step_click_apply_button(context):
    context.leave_page.click_apply_button()

@then('I should see the leave request in my leave list')
def step_verify_leave_request(context):
    # Navigate to My Leave
    context.leave_page.navigate_to_my_leave()
    
    # Verify the leave request is in the list
    assert context.leave_page.is_leave_request_visible(), "Leave request not found in the list"

@then('the status should be "{status}"')
def step_verify_status(context, status):
    assert context.leave_page.get_leave_status() == status, f"Leave status is not '{status}'"
