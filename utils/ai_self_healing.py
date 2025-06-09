import logging
import time
import json
import os
import re
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By

class AISelfHealingLocator:
    def __init__(self, name, element_description, *initial_locators):
        """
        Initialize with element description for AI-based healing
        
        :param name: Element name for logging
        :param element_description: Semantic description of the element (e.g., "username field", "login button")
        :param initial_locators: Tuples (by, value) in priority order
        """
        self.name = name
        self.element_description = element_description
        self.locator_strategies = list(initial_locators)
        self.successful_strategy = None
        self.failed_strategies = []
        
        # Debug logging to see what's being passed
        logging.debug(f"Created locator '{name}' with strategies: {self.locator_strategies}")
        
    def find_element(self, driver):
        """Try different strategies to find the element with AI enhancement"""
        # First check if we have learned strategies for this element
        if hasattr(driver, 'learned_locators') and self.name in driver.learned_locators:
            # Create a new list with learned strategies first, then original ones
            # Avoid duplicates
            strategies = []
            
            # Add learned strategies first
            for strategy in driver.learned_locators[self.name]:
                if strategy not in strategies:
                    strategies.append(strategy)
            
            # Then add original strategies
            for strategy in self.locator_strategies:
                if strategy not in strategies:
                    strategies.append(strategy)
                    
            # Replace the strategies list with our optimized one
            self.locator_strategies = strategies
            logging.info(f"Using learned locators for {self.name}: {strategies[0]}")
        
        # Now try all strategies
        for strategy_index, (by, value) in enumerate(self.locator_strategies):
            try:
                logging.debug(f"Trying to find '{self.name}' with {by}={value}")
                element = driver.find_element(by, value)
                
                # If this isn't the primary strategy but it worked, log it
                if strategy_index > 0:
                    logging.warning(
                        f"Self-healing activated for '{self.name}': "
                        f"Primary locator failed, using alternative: {by}={value}"
                    )
                    print(f"\n🔄 SELF-HEALING ACTIVATED for '{self.name}'")
                    print(f"   ❌ Failed locator: {self.locator_strategies[0]}")
                    print(f"   ✅ Successful locator: {by}={value}\n")
                else:
                    logging.debug(f"Found '{self.name}' with primary locator: {by}={value}")
                
                # Remember the successful strategy
                self.successful_strategy = (by, value)
                return element
                
            except (NoSuchElementException, StaleElementReferenceException):
                logging.debug(f"Failed to find '{self.name}' with {by}={value}")
                self.failed_strategies.append((by, value))
                continue
        
        # If all predefined strategies failed, try DOM analysis
        logging.warning(f"All predefined locators failed for '{self.name}'. Attempting DOM analysis...")
        print(f"\n⚠️ All predefined locators failed for '{self.name}'. Attempting AI DOM analysis...")
        
        # Analyze DOM to find potential elements
        ai_locators = self._analyze_dom_for_element(driver)
        
        # Try the AI-generated locators
        for by, value in ai_locators:
            try:
                element = driver.find_element(by, value)
                
                logging.warning(f"AI-generated locator successful for '{self.name}': {by}={value}")
                print(f"🤖 AI-GENERATED LOCATOR SUCCESSFUL: {by}={value}")
                
                # Remember the successful strategy
                self.successful_strategy = (by, value)
                
                # Add this to our strategies for future use
                if (by, value) not in self.locator_strategies:
                    self.locator_strategies.append((by, value))
                    
                return element
                
            except (NoSuchElementException, StaleElementReferenceException):
                continue
                
        # If we get here, all strategies failed
        strategies_tried = ', '.join([f"{by}='{value}'" for by, value in self.locator_strategies])
        logging.error(f"Self-healing failed for '{self.name}'. Tried: {strategies_tried}")
        raise NoSuchElementException(
            f"Self-healing failed for '{self.name}'. Tried: {strategies_tried}"
        )

    def _analyze_dom_for_element(self, driver):
        """
        Analyze the DOM to find potential matching elements when all locators fail
        
        :param driver: WebDriver instance
        :return: List of potential locator strategies
        """
        logging.info(f"Analyzing DOM to find '{self.name}' with description: {self.element_description}")
        print(f"\n🔍 AI ANALYSIS: Searching DOM for '{self.name}'...")
        
        potential_locators = []
        
        # Get page source for analysis
        page_source = driver.page_source
        
        # Extract all input elements
        if 'input' in self.element_description.lower() or 'field' in self.element_description.lower() or 'username' in self.element_description.lower() or 'password' in self.element_description.lower():
            # Try to find input elements
            input_pattern = re.compile(r'<input[^>]*>', re.IGNORECASE)
            inputs = input_pattern.findall(page_source)
            
            for input_html in inputs:
                # Check if this input matches our description
                if 'username' in self.element_description.lower() and ('username' in input_html.lower() or 'user' in input_html.lower() or 'email' in input_html.lower()):
                    # Extract attributes
                    id_match = re.search(r'id=["\'](.*?)["\']', input_html)
                    name_match = re.search(r'name=["\'](.*?)["\']', input_html)
                    class_match = re.search(r'class=["\'](.*?)["\']', input_html)
                    
                    if id_match:
                        potential_locators.append((By.ID, id_match.group(1)))
                    if name_match:
                        potential_locators.append((By.NAME, name_match.group(1)))
                    if class_match:
                        potential_locators.append((By.CLASS_NAME, class_match.group(1)))
                        
                elif 'password' in self.element_description.lower() and ('password' in input_html.lower() or 'pwd' in input_html.lower()):
                    # Extract attributes
                    id_match = re.search(r'id=["\'](.*?)["\']', input_html)
                    name_match = re.search(r'name=["\'](.*?)["\']', input_html)
                    class_match = re.search(r'class=["\'](.*?)["\']', input_html)
                    
                    if id_match:
                        potential_locators.append((By.ID, id_match.group(1)))
                    if name_match:
                        potential_locators.append((By.NAME, name_match.group(1)))
                    if class_match:
                        potential_locators.append((By.CLASS_NAME, class_match.group(1)))
        
        # Extract all button elements
        elif 'button' in self.element_description.lower() or 'login button' in self.element_description.lower():
            # Try to find button elements
            button_pattern = re.compile(r'<button[^>]*>.*?</button>', re.IGNORECASE | re.DOTALL)
            buttons = button_pattern.findall(page_source)
            
            for button_html in buttons:
                # Check if this button matches our description
                if 'login' in self.element_description.lower() and ('login' in button_html.lower() or 'sign in' in button_html.lower() or 'submit' in button_html.lower()):
                    # Extract attributes
                    id_match = re.search(r'id=["\'](.*?)["\']', button_html)
                    class_match = re.search(r'class=["\'](.*?)["\']', button_html)
                    type_match = re.search(r'type=["\'](.*?)["\']', button_html)
                    
                    if id_match:
                        potential_locators.append((By.ID, id_match.group(1)))
                    if class_match:
                        potential_locators.append((By.CLASS_NAME, class_match.group(1)))
                    if type_match and type_match.group(1) == 'submit':
                        potential_locators.append((By.CSS_SELECTOR, f"button[type='submit']"))
                    
                    # Extract button text
                    text_match = re.search(r'<button[^>]*>(.*?)</button>', button_html)
                    if text_match and text_match.group(1).strip():
                        text = text_match.group(1).strip()
                        potential_locators.append((By.XPATH, f"//button[contains(text(), '{text}')]"))
        
        # Add generic XPath locators based on element description keywords
        keywords = self.element_description.lower().split()
        for keyword in keywords:
            if len(keyword) > 3:  # Only use meaningful keywords
                potential_locators.append((By.XPATH, f"//*[contains(@id, '{keyword}')]"))
                potential_locators.append((By.XPATH, f"//*[contains(@name, '{keyword}')]"))
                potential_locators.append((By.XPATH, f"//*[contains(@class, '{keyword}')]"))
                potential_locators.append((By.XPATH, f"//*[contains(text(), '{keyword}')]"))
        
        # Add common locators for input fields
        if 'username' in self.element_description.lower():
            potential_locators.append((By.NAME, "username"))
            potential_locators.append((By.CSS_SELECTOR, "input[name='username']"))
            potential_locators.append((By.XPATH, "//input[@name='username']"))
            potential_locators.append((By.CSS_SELECTOR, "input[type='text']"))
            
        if 'password' in self.element_description.lower():
            potential_locators.append((By.NAME, "password"))
            potential_locators.append((By.CSS_SELECTOR, "input[name='password']"))
            potential_locators.append((By.XPATH, "//input[@name='password']"))
            potential_locators.append((By.CSS_SELECTOR, "input[type='password']"))
            
        if 'button' in self.element_description.lower() or 'login' in self.element_description.lower():
            potential_locators.append((By.CSS_SELECTOR, "button[type='submit']"))
            potential_locators.append((By.XPATH, "//button[@type='submit']"))
            potential_locators.append((By.XPATH, "//button[contains(text(), 'Login')]"))
        
        logging.info(f"DOM analysis found {len(potential_locators)} potential locators for '{self.name}'")
        print(f"🔍 AI ANALYSIS: Found {len(potential_locators)} potential locators for '{self.name}'")
        
        return potential_locators

class AISelfHealingDriver:
    def __init__(self, driver):
        """
        Initialize the self-healing driver
        
        :param driver: The Selenium WebDriver instance
        """
        self.driver = driver
        self.healing_stats = {
            "healed_count": 0,
            "failed_count": 0,
            "healing_events": []
        }
        self.learned_locators = {}  # Store learned locator strategies
        
        # Create reports directory if it doesn't exist
        if not os.path.exists("reports"):
            os.makedirs("reports")
            logging.info("Created reports directory")
        
        # Load any previously learned locators
        self.load_learned_locators()
        
    def find_element(self, locator):
        """
        Find element using AI self-healing locator
        
        :param locator: AISelfHealingLocator instance
        :return: WebElement
        """
        try:
            start_time = time.time()
            element = locator.find_element(self.driver)
            end_time = time.time()
            
            # If not using the primary strategy but it worked, count as healed
            if locator.successful_strategy != locator.locator_strategies[0]:
                self.healing_stats["healed_count"] += 1
                self.healing_stats["healing_events"].append({
                    "element": locator.name,
                    "description": locator.element_description,
                    "failed": locator.failed_strategies,
                    "succeeded": locator.successful_strategy,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "time_taken": end_time - start_time
                })
                
                # Learn from this successful healing
                self._learn_successful_strategy(locator)
                logging.info(f"Self-healing successful for '{locator.name}' using {locator.successful_strategy}")
                print(f"\n🔄 SELF-HEALING ACTIVATED for '{locator.name}'")
                print(f"   ❌ Failed locator: {locator.locator_strategies[0]}")
                print(f"   ✅ Successful locator: {locator.successful_strategy}\n")
                
            return element
            
        except NoSuchElementException as e:
            self.healing_stats["failed_count"] += 1
            self.healing_stats["healing_events"].append({
                "element": locator.name,
                "description": locator.element_description,
                "failed": locator.failed_strategies,
                "succeeded": None,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "error": str(e)
            })
            logging.error(f"Self-healing failed for '{locator.name}'. All strategies failed.")
            print(f"\n❌ SELF-HEALING FAILED for '{locator.name}'")
            print(f"   All {len(locator.failed_strategies)} locator strategies failed\n")
            raise
    
    def _learn_successful_strategy(self, locator):
        """
        Learn from successful healing events
        
        :param locator: AISelfHealingLocator that was successfully healed
        """
        if locator.name not in self.learned_locators:
            self.learned_locators[locator.name] = []
            
        # Add the successful strategy if not already present
        if locator.successful_strategy not in self.learned_locators[locator.name]:
            self.learned_locators[locator.name].insert(0, locator.successful_strategy)
            logging.info(f"Learned new strategy for '{locator.name}': {locator.successful_strategy}")
            print(f"📝 LEARNING: Added new strategy for '{locator.name}': {locator.successful_strategy}")
            
        # Keep only the top 3 most successful strategies
        self.learned_locators[locator.name] = self.learned_locators[locator.name][:3]
        
        # Save learned locators to file
        self._save_learned_locators()
        
    def _save_learned_locators(self):
        """Save learned locators to a file"""
        try:
            # Create reports directory if it doesn't exist
            if not os.path.exists("reports"):
                os.makedirs("reports")
                
            # Convert to serializable format
            serializable_locators = {}
            for name, strategies in self.learned_locators.items():
                serializable_locators[name] = []
                for by, value in strategies:
                    by_name = str(by).split('.')[-1]  # Extract name like 'NAME', 'ID', etc.
                    serializable_locators[name].append({"by": by_name, "value": value})
            
            # Save to file
            with open("reports/learned_locators.json", "w") as f:
                json.dump(serializable_locators, f, indent=2)
                
            logging.info(f"Saved learned locators for {len(self.learned_locators)} elements to reports/learned_locators.json")
        except Exception as e:
            logging.error(f"Error saving learned locators: {str(e)}")
    
    def load_learned_locators(self):
        """Load previously learned locators"""
        try:
            if os.path.exists("reports/learned_locators.json"):
                with open("reports/learned_locators.json", "r") as f:
                    serialized = json.load(f)
                    
                # Convert back to tuples
                for name, strategies in serialized.items():
                    self.learned_locators[name] = []
                    for strategy in strategies:
                        try:
                            by_attr = getattr(By, strategy["by"])
                            self.learned_locators[name].append((by_attr, strategy["value"]))
                        except AttributeError:
                            logging.warning(f"Unknown locator type: {strategy['by']} for element {name}")
                            continue
                            
                logging.info(f"Loaded learned locators for {len(self.learned_locators)} elements")
                print(f"📚 Loaded {len(self.learned_locators)} learned locator strategies from previous runs")
            else:
                logging.info("No learned locators file found. Starting fresh.")
        except Exception as e:
            logging.error(f"Error loading learned locators: {str(e)}")
            
    def get_healing_report(self):
        """
        Return a report of self-healing statistics
        
        :return: Dictionary with healing statistics and events
        """
        total_attempts = self.healing_stats["healed_count"] + self.healing_stats["failed_count"]
        success_rate = (self.healing_stats["healed_count"] / (total_attempts or 1)) * 100
        
        return {
            "summary": {
                "total_attempts": total_attempts,
                "successful_healing": self.healing_stats["healed_count"],
                "failed_healing": self.healing_stats["failed_count"],
                "success_rate": success_rate
            },
            "events": self.healing_stats["healing_events"]
        }
        
    def generate_html_report(self, filename="reports/healing_report.html"):
        """
        Generate an HTML report of self-healing activities
        
        :param filename: Path to save the HTML report
        :return: Path to the generated report
        """
        report = self.get_healing_report()
        
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Self-Healing Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1 { color: #2c3e50; }
                .summary { background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
                .event { background-color: #ffffff; padding: 15px; border-radius: 5px; margin-bottom: 10px; border-left: 5px solid #3498db; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
                .success { border-left-color: #2ecc71; }
                .failure { border-left-color: #e74c3c; }
                .strategies { font-family: monospace; background-color: #f8f9fa; padding: 10px; border-radius: 3px; }
                .timestamp { color: #7f8c8d; font-size: 0.9em; }
            </style>
        </head>
        <body>
            <h1>Self-Healing Test Report</h1>
            
            <div class="summary">
                <h2>Summary</h2>
                <p>Total Attempts: {total}</p>
                <p>Successful Healing: {success} ({rate:.1f}%)</p>
                <p>Failed Healing: {failed}</p>
            </div>
            
            <h2>Healing Events</h2>
        """.format(
            total=report["summary"]["total_attempts"],
            success=report["summary"]["successful_healing"],
            failed=report["summary"]["failed_healing"],
            rate=report["summary"]["success_rate"]
        )
        
        for event in report["events"]:
            event_class = "success" if event["succeeded"] else "failure"
            
            html += """
            <div class="event {event_class}">
                <h3>{element}</h3>
                <p><strong>Description:</strong> {description}</p>
                <p><strong>Failed Strategies:</strong></p>
                <div class="strategies">
                    {failed_strategies}
                </div>
                <p><strong>Successful Strategy:</strong></p>
                <div class="strategies">
                    {succeeded_strategy}
                </div>
                <p class="timestamp">{timestamp} (took {time_taken:.3f}s)</p>
            </div>
            """.format(
                event_class=event_class,
                element=event["element"],
                description=event.get("description", ""),
                failed_strategies="<br>".join([f"{by}='{value}'" for by, value in event["failed"]]) if event["failed"] else "None",
                succeeded_strategy=f"{event['succeeded'][0]}='{event['succeeded'][1]}'" if event["succeeded"] else "None",
                timestamp=event["timestamp"],
                time_taken=event.get("time_taken", 0)
            )
        
        html += """
        </body>
        </html>
        """
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, "w") as f:
            f.write(html)
            
        logging.info(f"Generated HTML report: {filename}")
        print(f"📊 Generated HTML report: {filename}")
        return filename
    
    
  
def generate_dashboard(self, filename="reports/dashboard.html"):
    """
    Generate a dashboard with charts for healing statistics

    :param filename: Path to save the dashboard
    :return: Path to the generated dashboard
    """
    try:
        report = self.get_healing_report()

        # Calculate statistics
        total = report["summary"]["total_attempts"]
        healed = report["summary"]["successful_healing"]
        failed = report["summary"]["failed_healing"]
        success_rate = report["summary"]["success_rate"]

        # Get element-specific stats
        element_stats = {}
        for event in report["events"]:
            element_name = event["element"]
            if element_name not in element_stats:
                element_stats[element_name] = {"healed": 0, "failed": 0}

            if event["succeeded"]:
                element_stats[element_name]["healed"] += 1
            else:
                element_stats[element_name]["failed"] += 1

        # Prepare data for charts
        element_labels = list(element_stats.keys()) if element_stats else []
        element_success = [stats["healed"] for stats in element_stats.values()] if element_stats else []
        element_failed = [stats["failed"] for stats in element_stats.values()] if element_stats else []

        # Default values if no data
        if not element_labels:
            element_labels = ["No Data"]
            element_success = [0]
            element_failed = [0]

        # Generate HTML
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Self-Healing Dashboard</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1 { color: #2c3e50; }
                .stats { display: flex; justify-content: space-between; margin-bottom: 20px; }
                .stat-card { background-color: #f8f9fa; padding: 15px; border-radius: 5px; width: 23%; text-align: center; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
                .stat-value { font-size: 24px; font-weight: bold; margin: 10px 0; }
                .success { color: #2ecc71; }
                .failure { color: #e74c3c; }
                .chart { background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px; height: 300px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
                .chart-container { display: flex; justify-content: space-between; }
                .chart-half { width: 48%; }
                .no-data { text-align: center; padding: 50px; color: #7f8c8d; }
            </style>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        </head>
        <body>
            <h1>Self-Healing Dashboard</h1>

            <div class="stats">
                <div class="stat-card">
                    <h3>Total Attempts</h3>
                    <div class="stat-value">{total}</div>
                </div>
                <div class="stat-card">
                    <h3>Successful Healing</h3>
                    <div class="stat-value success">{healed}</div>
                </div>
                <div class="stat-card">
                    <h3>Failed Healing</h3>
                    <div class="stat-value failure">{failed}</div>
                </div>
                <div class="stat-card">
                    <h3>Success Rate</h3>
                    <div class="stat-value">{rate:.1f}%</div>
                </div>
            </div>

            <div class="chart-container">
                <div class="chart chart-half">
                    <canvas id="healingChart"></canvas>
                </div>
                <div class="chart chart-half">
                    <canvas id="elementsChart"></canvas>
                </div>
            </div>

            <script>
                // Create healing chart
                const ctxHealing = document.getElementById('healingChart').getContext('2d');
                const healingChart = new Chart(ctxHealing, {{
                    type: 'pie',
                    data: {{
                        labels: ['Successful Healing', 'Failed Healing'],
                        datasets: [{{
                            data: [{healed}, {failed}],
                            backgroundColor: ['#2ecc71', '#e74c3c']
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            title: {{
                                display: true,
                                text: 'Healing Success Rate',
                                font: {{ size: 16 }}
                            }}
                        }}
                    }}
                }});

                // Create elements chart
                const ctxElements = document.getElementById('elementsChart').getContext('2d');
                const elementsChart = new Chart(ctxElements, {{
                    type: 'bar',
                    data: {{
                        labels: {element_labels},
                        datasets: [
                            {{
                                label: 'Successful Healing',
                                data: {element_success},
                                backgroundColor: '#2ecc71'
                            }},
                            {{
                                label: 'Failed Healing',
                                data: {element_failed},
                                backgroundColor: '#e74c3c'
                            }}
                        ]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            title: {{
                                display: true,
                                text: 'Healing by Element',
                                font: {{ size: 16 }}
                            }}
                        }},
                        scales: {{
                            x: {{
                                stacked: true
                            }},
                            y: {{
                                stacked: true,
                                beginAtZero: true
                            }}
                        }}
                    }}
                }});
            </script>
        </body>
        </html>
        """.format(
            total=total,
            healed=healed,
            failed=failed,
            rate=success_rate,
            element_labels=json.dumps(element_labels),
            element_success=json.dumps(element_success),
            element_failed=json.dumps(element_failed)
        )

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, "w") as f:
            f.write(html)

        logging.info(f"Generated dashboard: {filename}")
        print(f"📊 Generated dashboard: {filename}")
        return filename

    except Exception as e:
        logging.error(f"Error generating dashboard: {str(e)}")
        print(f"❌ Error generating dashboard: {str(e)}")

        # Create a simple error dashboard
        error_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Dashboard Error</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #e74c3c; }}
                .error {{ background-color: #f8d7da; padding: 15px; border-radius: 5px; color: #721c24; }}
            </style>
        </head>
        <body>
            <h1>Error Generating Dashboard</h1>
            <div class="error">
                <p>An error occurred while generating the dashboard:</p>
                <pre>{str(e)}</pre>
            </div>
        </body>
        </html>
        """

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, "w") as f:
            f.write(error_html)

        return filename
    
 

def analyze_locators(self):
    """
    Analyze the current state of locators and provide recommendations
    
    :return: Dictionary with analysis results
    """
    analysis = {
        "most_healed_elements": [],
        "most_reliable_strategies": {},
        "least_reliable_strategies": {},
        "recommendations": []
    }
    
    # Count healing events by element
    element_counts = {}
    strategy_success = {}
    strategy_failure = {}
    
    for event in self.healing_stats["healing_events"]:
        element_name = event["element"]
        if element_name not in element_counts:
            element_counts[element_name] = 0
        element_counts[element_name] += 1
        
        # Track strategy success/failure
        if event["succeeded"]:
            by, value = event["succeeded"]
            strategy_key = str(by)
            
            if strategy_key not in strategy_success:
                strategy_success[strategy_key] = 0
            strategy_success[strategy_key] += 1
        
        for by, value in event["failed"]:
            strategy_key = str(by)
            
            if strategy_key not in strategy_failure:
                strategy_failure[strategy_key] = 0
            strategy_failure[strategy_key] += 1
    
    # Find most healed elements
    if element_counts:
        sorted_elements = sorted(element_counts.items(), key=lambda x: x[1], reverse=True)
        analysis["most_healed_elements"] = sorted_elements[:3]
        
        # Add recommendations for most healed elements
        for element, count in sorted_elements[:3]:
            analysis["recommendations"].append(
                f"Consider updating the primary locator for '{element}' as it required healing {count} times."
            )
    
    # Calculate strategy reliability
    strategy_reliability = {}
    for strategy in set(list(strategy_success.keys()) + list(strategy_failure.keys())):
        success = strategy_success.get(strategy, 0)
        failure = strategy_failure.get(strategy, 0)
        total = success + failure
        
        if total > 0:
            reliability = (success / total) * 100
            strategy_reliability[strategy] = reliability
    
    # Find most and least reliable strategies
    if strategy_reliability:
        sorted_strategies = sorted(strategy_reliability.items(), key=lambda x: x[1], reverse=True)
        analysis["most_reliable_strategies"] = dict(sorted_strategies[:3])
        analysis["least_reliable_strategies"] = dict(sorted_strategies[-3:])
        
        # Add recommendations for strategies
        most_reliable = sorted_strategies[0][0] if sorted_strategies else None
        least_reliable = sorted_strategies[-1][0] if sorted_strategies else None
        
        if most_reliable and least_reliable:
            analysis["recommendations"].append(
                f"Consider using {most_reliable} as primary locator strategy instead of {least_reliable} where possible."
            )
    
    # Add learned locator recommendations
    if self.learned_locators:
        analysis["recommendations"].append(
            f"You have {len(self.learned_locators)} learned locator strategies that can be used to update your source code."
        )
    
    return analysis
def update_source_code_locators(self, file_path):
    """
    Update locators in source code based on learned strategies
    
    :param file_path: Path to the source file (e.g., login_page.py)
    :return: True if successful, False otherwise
    """
    if not hasattr(self, 'learned_locators') or not self.learned_locators:
        print("ℹ️ No learned locators to update source code with")
        return False
        
    try:
        print(f"🔍 Attempting to update locators in {file_path}")
        
        # Read the source file
        with open(file_path, 'r') as f:
            lines = f.readlines()
            
        # Track if we made any changes
        changes_made = False
        
        # Process the file line by line
        for i, line in enumerate(lines):
            # Look for create_ai_locator calls
            if 'create_ai_locator' in line:
                # Extract the element name
                name_match = re.search(r'["\'](.*?)["\']', line)
                if name_match:
                    element_name = name_match.group(1)
                    print(f"🔍 Found element in source code: {element_name}")
                    
                    # Check if we have learned locators for this element
                    if element_name in self.learned_locators and self.learned_locators[element_name]:
                        print(f"🔍 Found learned locators for {element_name}: {self.learned_locators[element_name]}")
                        
                        # Find the closing parenthesis of this call
                        j = i
                        parenthesis_count = line.count('(') - line.count(')')
                        while parenthesis_count > 0 and j < len(lines) - 1:
                            j += 1
                            parenthesis_count += lines[j].count('(') - lines[j].count(')')
                        
                        if j > i:
                            # We found a multi-line create_ai_locator call
                            print(f"🔍 Found multi-line create_ai_locator call from line {i} to {j}")
                            
                            # Find the line with the first locator
                            first_locator_line = None
                            for line_idx in range(i+1, j):
                                if '(' in lines[line_idx] and ')' in lines[line_idx] and 'By.' in lines[line_idx]:
                                    first_locator_line = line_idx
                                    break
                            
                            if first_locator_line is not None:
                                print(f"🔍 First locator line: {first_locator_line}, content: {lines[first_locator_line].strip()}")
                                
                                # Get the best learned locator
                                best_locator = self.learned_locators[element_name][0]
                                by_type, value = best_locator
                                
                                # Convert by_type to string representation
                                if isinstance(by_type, str):
                                    by_str = by_type
                                else:
                                    by_str = str(by_type).split('.')[-1]
                                
                                # Create the locator string
                                best_locator_str = f"(By.{by_str}, '{value}')"
                                
                                # Check if the best learned locator is different from the current primary
                                current_primary = lines[first_locator_line].strip()
                                if best_locator_str not in current_primary:
                                    print(f"🔍 Best locator {best_locator_str} is different from current primary {current_primary}")
                                    
                                    # Replace the primary locator with the best learned one
                                    indent = len(lines[first_locator_line]) - len(lines[first_locator_line].lstrip())
                                    new_line = ' ' * indent + best_locator_str + ',  # AI-learned primary locator\n'
                                    lines[first_locator_line] = new_line
                                    
                                    changes_made = True
                                    print(f"📝 UPDATED SOURCE CODE: Primary locator for '{element_name}' is now {best_locator_str}")
                                else:
                                    print(f"🔍 Best locator is already the primary one")
                            else:
                                print(f"⚠️ Could not find first locator line")
        
        # Write the modified file if changes were made
        if changes_made:
            with open(file_path, 'w') as f:
                f.writelines(lines)
            print(f"✅ Successfully updated source code in {file_path}")
            return True
        else:
            print(f"ℹ️ No locator updates needed in {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error updating source code: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
