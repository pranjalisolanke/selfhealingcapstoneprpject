Feature: OrangeHRM Timesheet Management

    Scenario: Add and submit timesheet entry with AI-enhanced locators
        Given I am logged in as an admin
        When I navigate to time module
        And I enter text in employee name textbox
        And I click on the view button
        Then I verify the timesheet status
       
