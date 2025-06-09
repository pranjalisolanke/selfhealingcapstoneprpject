Feature: AI-Enhanced Self-Healing Login

  Scenario: Login with AI-powered self-healing locators
    Given I am on the Orange HRM login page
    When I enter "Admin" as username using AI-enhanced locators
    And I enter "admin123" as password using AI-enhanced locators
    And I click on the login button using intelligent locator detection
    Then I should be logged in successfully
    And I should see the dashboard