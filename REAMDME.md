# Self-Healing Selenium Python Framework for OrangeHRM

## Overview

This project implements a self-healing Selenium automation framework for testing the OrangeHRM application. The framework uses AI-powered locator strategies to automatically recover from broken locators, making tests more resilient to UI changes.

## Features

- **Self-Healing Locators**: Automatically recovers from broken locators using AI-based DOM analysis
- **Multi-Strategy Approach**: Uses multiple locator strategies for each element
- **Locator Learning**: Learns successful locator strategies and updates test code
- **Comprehensive Logging**: Detailed logging of all test actions and healing events
- **Page Object Model**: Well-structured page objects for better maintainability
- **BDD Integration**: Uses Behave for behavior-driven development

## 🧠 Self-Healing Mechanism

The framework uses a **multi-layered approach** to locate elements:

1. **Primary Locator**: Attempts to find the element using the primary locator
2. **Alternative Locators**: If the primary fails, tries fallback locators
3. **AI DOM Analysis**: If all locators fail, analyzes the DOM to generate new ones
4. **Locator Learning**: Saves successful fallback locators for future runs
5. **Code Update**: Automatically integrates learned locators into test code

### 🔍 Example:

self.employee_name_input = self.create_ai_locator(
    "employee_name_input",
    "Employee name input field on timesheet page",
    (By.XPATH, "//div[contains(@class,'oxd-autocomplete-text-input')]/input[@placeholder='Type for hints...']"),
    [
        (By.CSS_SELECTOR, "div.oxd-autocomplete-text-input input"),
        (By.XPATH, "//input[@placeholder='Type for hints...']"),
        (By.CSS_SELECTOR, ".oxd-autocomplete-text-input--active input")
    ]
)

## 🛠 Troubleshooting
# Element Not Found: Check if the locator is correct or if the page structure has changed
 - All predefined locators failed for 'element_name'. Attempting AI DOM analysis...

# Timeouts: Increase the timeout value in the wait methods
- self.wait_for_element_visible(self.element, timeout=30)

# Stale Element Reference: The element was found but became stale before interaction
- StaleElementReferenceException: Message: stale element reference


## Project Structure

├── drivers/                      # WebDriver executables
├── features/                     # BDD feature files and steps
│   ├── steps/                    # Step definitions
│   ├── employee_management.feature
│   ├── environment.py            # Behave environment setup
│   ├── leave_management.feature
│   ├── login.feature
│   └── timesheet.feature
├── pages/                        # Page Object Models
│   ├── __pycache__/
│   ├── base_page.py              # Base page with self-healing functionality
│   ├── dashboard_page.py
│   ├── leave_page.py
│   ├── login_page.py
│   ├── pim_page.py
│   └── timesheet_page.py
├── reports/                      # Test reports and logs
│   ├── index.html
│   ├── learned_locators.json     # Learned locator strategies
│   ├── self_healing_report.html
│   └── self_healing.log
├── utils/                        # Utility modules
├── venv/                         # Virtual environment
├── .env                          # Environment variables
├── config.py                     # Configuration settings
├── generate_self_healing_html_report.py
├── merge_html_reports.py
├── README.md
└── requirements.txt              # Project dependencies


## Installation

# Install Python 
# For Windows
- sudo apt install python3 python3-pip python3-venv

# Create virtual environment
- python -m venv venv
- venv\Scripts\activate

# Install core packages
- pip install selenium
- pip install behave

# Install packages for DOM analysis and self-healing
- pip install cssselect
- pip install html5lib
- pip install difflib
- pip install scikit-learn
- pip install nltk
- pip install jinja2

# Install reporting packages
- pip install behave-html-formatter

# Command to run tests
- Run all tests : behave
- Run specific test : behave features/timesheet.feature
- python generate_self_healing_html_report.py

## Configuration
- Update environment variables in .env file:
- BASE_URL=https://opensource-demo.orangehrmlive.com/
- ADMIN_USERNAME=Admin
- ADMIN_PASSWORD=admin123
- HEADLESS=False