# features/leave_management.feature
Feature: Leave Management with AI Self-Healing

  Scenario: Apply for leave with AI-enhanced locators
    Given I am logged in as an admin
    When I navigate to the Leave module
    And I click on my leave
    And I select leave details
      | Leave Type    | From Date  | To Date    |
      | US - Vacation | 2025-07-01 | 2025-07-05 |
    Then I click on search


