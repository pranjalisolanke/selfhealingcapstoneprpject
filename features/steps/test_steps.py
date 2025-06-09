from behave import given, when, then
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

@given('I am on the Orange HRM login page')
def step_navigate_to_login_page(context):
    context.login_page = LoginPage(context.driver)
    context.login_page.navigate_to("https://opensource-demo.orangehrmlive.com/")

@when('I enter "{username}" as username using AI-enhanced locators')
def step_enter_username(context, username):
    context.login_page.input_text(context.login_page.username_field, username)

@when('I enter "{password}" as password using AI-enhanced locators')
def step_enter_password(context, password):
    context.login_page.input_text(context.login_page.password_field, password)

@when('I click on the login button using intelligent locator detection')
def step_click_login(context):
    context.login_page.click(context.login_page.login_button)
    
    # Create the dashboard page after clicking login
    context.dashboard_page = DashboardPage(context.driver)
    
    # Wait for dashboard to load
    context.dashboard_page.wait_for_page_load()

@then('I should be logged in successfully')
def step_verify_login_success(context):
    # Check if the user dropdown is visible (indicates successful login)
    assert context.dashboard_page.is_element_visible(context.dashboard_page.user_dropdown), "Login failed - user dropdown not visible"

@then('I should see the dashboard')
def step_verify_dashboard(context):
    assert context.dashboard_page.is_dashboard_loaded(), "Dashboard did not load correctly"
