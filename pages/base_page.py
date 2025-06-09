from utils.ai_self_healing import AISelfHealingLocator

class BasePage:
    def __init__(self, driver):
        self.driver = driver
    
    def create_ai_locator(self, name, description, *strategies):
        """
        Create an AI-enhanced self-healing locator
        
        :param name: Name of the element for reporting
        :param description: Description of the element for AI analysis
        :param strategies: Tuple locator strategies (By.TYPE, "value")
        :return: AISelfHealingLocator instance
        """
        # Make sure we're passing the strategies correctly
        return AISelfHealingLocator(name, description, *strategies)
    
    def click(self, locator):
        """Click on an element with AI self-healing"""
        element = self.driver.find_element(locator)
        element.click()
    
    def input_text(self, locator, text):
        """Input text with AI self-healing"""
        element = self.driver.find_element(locator)
        element.clear()
        element.send_keys(text)

    def clear_and_input_text(self, locator, text):
        """Clear the input field and enter text with AI self-healing"""
        element = self.driver.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator):
        """Get text with AI self-healing"""
        element = self.driver.find_element(locator)
        return element.text
    
    def is_displayed(self, locator):
        """Check if element is displayed with AI self-healing"""
        try:
            element = self.driver.find_element(locator)
            return element.is_displayed()
        except:
            return False
