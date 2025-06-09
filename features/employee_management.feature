# features/employee_management.feature
Feature: Employee Management with AI Self-Healing

  Scenario: Add a new employee with AI self-healing locators
    Given I am logged in as an admin
    When I navigate to the PIM module
    And I click on "Add Employee"
    And I enter employee details
      | First Name | Middle Name | Last Name | Employee ID |
      | John       | David       | Smith     | EMP001      |
    And I click Save
    Then I should see a success message
    

