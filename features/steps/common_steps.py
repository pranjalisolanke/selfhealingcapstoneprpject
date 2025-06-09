# features/steps/common_steps.py
from behave import given
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

@given('I am logged in as an admin')
def step_login_as_admin(context):
    login_page = LoginPage(context.driver)
    login_page.navigate_to("https://opensource-demo.orangehrmlive.com/")
    login_page.login("Admin", "admin123")
    
    # Verify we're on the dashboard
    context.dashboard_page = DashboardPage(context.driver)
    assert context.dashboard_page.is_element_visible(context.dashboard_page.user_dropdown), "Login failed"
