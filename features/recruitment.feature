Feature: OrangeHRM Recruitment Management

    Scenario: Add a new candidate with AI-enhanced locators
        Given I am logged in as an admin
        When I navigate to recruitment module
        And I click on the add button
        And I enter candidate details
            | First Name | Middle Name | Last Name | Email              | Vacancy           |
            | John       | William     | Smith     | jsmith@example.com | Software Engineer |
        And I click on the save button
        Then I should see a success toast message
        And the candidate should be added to the list
