from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from utils.ai_self_healing import AISelfHealingDriver
import os

def create_driver(browser_name="chrome", headless=False):
    """Create a WebDriver instance based on browser name using local driver files"""
    browser_name = browser_name.lower()
    
    # Get the path to the drivers folder
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    drivers_folder = os.path.join(project_root, "drivers")
    
    try:
        if browser_name == "chrome":
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument("--headless")
            
            # Use local ChromeDriver
            chromedriver_path = os.path.join(drivers_folder, "chromedriver.exe")
            print(f"Using ChromeDriver at: {chromedriver_path}")
            
            if not os.path.exists(chromedriver_path):
                raise FileNotFoundError(f"ChromeDriver not found at {chromedriver_path}")
                
            service = ChromeService(executable_path=chromedriver_path)
            driver = webdriver.Chrome(service=service, options=options)
        
        elif browser_name == "edge":
            options = webdriver.EdgeOptions()
            if headless:
                options.add_argument("--headless")
            
            # Use local EdgeDriver
            edgedriver_path = os.path.join(drivers_folder, "msedgedriver.exe")
            print(f"Using EdgeDriver at: {edgedriver_path}")
            
            if not os.path.exists(edgedriver_path):
                raise FileNotFoundError(f"EdgeDriver not found at {edgedriver_path}")
                
            service = EdgeService(executable_path=edgedriver_path)
            driver = webdriver.Edge(service=service, options=options)
        
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")
        
        driver.maximize_window()
        
        # Wrap the driver with our self-healing driver
        return AISelfHealingDriver(driver)
    
    except Exception as e:
        print(f"Error creating driver: {str(e)}")
        raise
