import os
import json
import re
import traceback
from datetime import datetime
from utils.driver_factory import create_driver
from utils.code_updater import update_source_code_with_locators  # Import the function

# --- NEW: Load .env and set OpenAI key ---
from dotenv import load_dotenv
import openai

load_dotenv()  # Loads .env file if present

def before_all(context):
    """Set up environment before all tests"""
    # Load OpenAI API key from environment
    context.openai_api_key = os.environ.get("OPENAI_API_KEY")
    openai.api_key = context.openai_api_key
    print("OpenAI API key loaded:", bool(context.openai_api_key))

    # Create a directory for reports if it doesn't exist
    if not os.path.exists("reports"):
        os.makedirs("reports")
        print("📁 Created reports directory")
    
    # Create a directory for drivers if it doesn't exist
    if not os.path.exists("drivers"):
        os.makedirs("drivers")
        print("📁 Created drivers directory")
        print("⚠️ Please download the appropriate browser drivers and place them in the 'drivers' folder.")

def before_scenario(context, scenario):
    """Set up environment before each scenario"""
    print(f"\n{'='*80}")
    print(f"🚀 RUNNING SCENARIO: {scenario.name}")
    print(f"{'='*80}")
    
    # Create a driver for each scenario
    try:
        # Try Chrome first
        context.driver = create_driver("chrome")
        context.driver.driver.implicitly_wait(10)
        print("🌐 Using Chrome browser")
    except Exception as e:
        print(f"⚠️ Error creating Chrome driver: {str(e)}")
        try:
            # Fall back to Edge if Chrome fails
            context.driver = create_driver("edge")
            context.driver.driver.implicitly_wait(10)
            print("🌐 Using Edge browser")
        except Exception as e2:
            print(f"❌ Error creating Edge driver: {str(e2)}")
            raise

def after_scenario(context, scenario):
    """Clean up and report after each scenario"""
    print(f"\n{'='*80}")
    print(f"📊 SCENARIO COMPLETED: {scenario.name}")
    print(f"{'='*80}")
    
    # Generate healing report after each scenario
    if hasattr(context, 'driver'):
        try:
            # Create timestamp and scenario name for file naming
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            scenario_name = scenario.name.replace(' ', '_').lower()
            
            # Save healing report as JSON
            try:
                report = context.driver.get_healing_report()
                json_report_path = f"reports/healing_report_{scenario_name}_{timestamp}.json"
                with open(json_report_path, 'w') as f:
                    json.dump(report, f, indent=2)
                print(f"📄 JSON report saved: {json_report_path}")
            except Exception as e:
                print(f"⚠️ Error saving JSON report: {str(e)}")
            
            # Print healing summary
            print_healing_summary(context.driver)
            
            # Check for learned locators and update source code
            if hasattr(context.driver, 'learned_locators') and context.driver.learned_locators:
                print("\n🔄 LEARNED LOCATORS:")
                for element, strategies in context.driver.learned_locators.items():
                    if strategies:
                        print(f"  • {element}: {strategies[0]}")
                
                # Update source code with learned locators using the separate function
                print("\n📝 Updating source code with learned locators...")
                try:
                    # Use the imported function instead of a method on the driver
                    result = update_source_code_with_locators("pages/login_page.py", context.driver.learned_locators)
                    if result:
                        print("✅ Source code updated successfully")
                    else:
                        print("ℹ️ No source code updates were needed")
                except Exception as e:
                    print(f"⚠️ Error updating source code: {str(e)}")
                    traceback.print_exc()
            else:
                print("\nℹ️ No learned locators available")
            
            # Take screenshot if scenario failed
            if scenario.status == "failed":
                try:
                    screenshot_path = f"reports/failure_{scenario_name}_{timestamp}.png"
                    context.driver.driver.save_screenshot(screenshot_path)
                    print(f"📷 Failure screenshot saved: {screenshot_path}")
                except Exception as e:
                    print(f"⚠️ Error saving screenshot: {str(e)}")
            
            # Print scenario status
            if scenario.status == "passed":
                print("\n✅ SCENARIO PASSED")
            else:
                print("\n❌ SCENARIO FAILED")
                
        except Exception as e:
            print(f"⚠️ Error in after_scenario: {str(e)}")
            traceback.print_exc()
        
        finally:
            # Always try to close the driver
            try:
                context.driver.driver.quit()
                print("🔒 Browser closed")
            except Exception as e:
                print(f"⚠️ Error closing browser: {str(e)}")

def print_healing_summary(driver):
    """Print a summary of healing and learning activities"""
    try:
        # Get healing report
        report = driver.get_healing_report()
        
        print("\n" + "-"*80)
        print("📊 SELF-HEALING SUMMARY")
        print("-"*80)
        
        # Print healing statistics
        total = report["summary"]["total_attempts"]
        healed = report["summary"]["successful_healing"]
        failed = report["summary"]["failed_healing"]
        
        print(f"📈 HEALING STATISTICS:")
        print(f"  • Total Attempts: {total}")
        print(f"  • Successful Healing: {healed}")
        print(f"  • Failed Healing: {failed}")
        
        # Calculate and print success rate
        if total > 0:
            success_rate = (healed / total) * 100
            print(f"  • Success Rate: {success_rate:.1f}%")
        else:
            print(f"  • Success Rate: N/A (no attempts)")
        
        # Print healing events
        if report["events"]:
            print(f"\n🔄 HEALING EVENTS:")
            for i, event in enumerate(report["events"]):
                print(f"  Event {i+1}:")
                print(f"    • Element: {event['element']}")
                print(f"    • Description: {event.get('description', 'N/A')}")
                print(f"    • Failed Strategies: {len(event['failed'])}")
                if event["succeeded"]:
                    print(f"    • Successful Strategy: {event['succeeded'][0]}='{event['succeeded'][1]}'")
                else:
                    print(f"    • Successful Strategy: None (healing failed)")
                print(f"    • Timestamp: {event['timestamp']}")
        
        print("-"*80)
    except Exception as e:
        print(f"⚠️ Error printing healing summary: {str(e)}")
        traceback.print_exc()
