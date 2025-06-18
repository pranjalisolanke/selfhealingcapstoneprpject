from behave import given, when, then
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.leave_page import LeavePage

@when('I navigate to the Leave module')
def step_navigate_to_leave(context):
    dashboard_page = DashboardPage(context.driver)
    dashboard_page.navigate_to_leave()
    context.leave_page = LeavePage(context.driver)

@when('I click on my leave')
def step_click_my_leave(context):
    context.leave_page.click_my_leave()

@when('I select leave details')
def step_select_leave_details(context):
    # Get the first row of data (excluding header)
    row = context.table[0]
    leave_type = row['Leave Type']
    from_date = row['From Date']
    to_date = row['To Date']
    context.leave_page.select_leave_type(leave_type)
    context.leave_page.set_from_date(from_date)
    context.leave_page.set_to_date(to_date)

@then('I click on search')
def step_click_search(context):
    context.leave_page.click_search_button()

@then('I should see the leave request in my leave list')
def step_verify_leave_request(context):
    context.leave_page.navigate_to_my_leave()
    assert context.leave_page.is_leave_request_visible(), "Leave request not found in the list"

@then('the status should be "{status}"')
def step_verify_status(context, status):
    assert context.leave_page.get_leave_status() == status, f"Leave status is not '{status}'"
