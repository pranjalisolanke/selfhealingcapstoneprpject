# features/leave_management.feature
Feature: Leave Management with AI Self-Healing

  Scenario: Apply for leave with AI-enhanced locators
    Given I am logged in as an employee
    When I navigate to the Leave module
    And I click on "Apply"
    And I select leave details:
      | Leave Type | From Date  | To Date    | Comments          |
      | Vacation   | 2025-07-01 | 2025-07-05 | Summer vacation   |
    And I click Apply
    Then I should see the leave request in my leave list
    And the status should be "Pending Approval"
