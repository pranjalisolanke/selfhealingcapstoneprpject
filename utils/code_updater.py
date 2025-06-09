import re
import os
import traceback
from selenium.webdriver.common.by import By

def update_source_code_with_locators(file_path, learned_locators):
    """
    Update locators in source code based on learned strategies
    
    :param file_path: Path to the source file (e.g., login_page.py)
    :param learned_locators: Dictionary of learned locators
    :return: True if successful, False otherwise
    """
    if not learned_locators:
        print("ℹ️ No learned locators to update source code with")
        return False
        
    try:
        print(f"🔍 Attempting to update locators in {file_path}")
        
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path} (current directory: {os.getcwd()})")
            return False
        
        # Create a backup of the original file with UTF-8 encoding
        backup_path = f"{file_path}.bak"
        try:
            with open(file_path, 'r', encoding='utf-8') as src, open(backup_path, 'w', encoding='utf-8') as dst:
                dst.write(src.read())
            print(f"📑 Created backup at {backup_path}")
        except UnicodeDecodeError:
            # Try with latin-1 encoding which can read any byte sequence
            try:
                with open(file_path, 'r', encoding='latin-1') as src, open(backup_path, 'w', encoding='utf-8') as dst:
                    content = src.read()
                    # Convert to UTF-8 for consistent processing
                    dst.write(content)
                print(f"📑 Created backup at {backup_path} (converted from latin-1 to utf-8)")
            except Exception as e:
                print(f"⚠️ Warning: Could not create backup: {str(e)}")
        except Exception as e:
            print(f"⚠️ Warning: Could not create backup: {str(e)}")
        
        # Read the source file with UTF-8 encoding
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.splitlines(True)  # Keep line endings
        except UnicodeDecodeError:
            # Fall back to latin-1 encoding
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
                lines = content.splitlines(True)  # Keep line endings
        
        # Track if we made any changes
        changes_made = False
        
        # Process the file line by line to find locator definitions
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Look for create_ai_locator calls
            if 'create_ai_locator' in line and 'self.' in line:
                # Extract the element name using a more precise pattern
                name_match = re.search(r'self\.([a-zA-Z0-9_]+)\s*=\s*self\.create_ai_locator', line)
                if name_match:
                    element_name = name_match.group(1)
                    print(f"🔍 Found element in source code: {element_name}")
                    
                    # Check if we have learned locators for this element
                    if element_name in learned_locators and learned_locators[element_name]:
                        print(f"🔍 Found learned locators for {element_name}: {learned_locators[element_name]}")
                        
                        # Find the end of this locator definition (closing parenthesis)
                        start_line = i
                        parenthesis_count = line.count('(') - line.count(')')
                        j = i
                        
                        while parenthesis_count > 0 and j < len(lines) - 1:
                            j += 1
                            parenthesis_count += lines[j].count('(') - lines[j].count(')')
                        
                        # Now we have the full locator definition from line i to j
                        
                        # Find the line with the first locator (By.X, "value")
                        first_locator_line = None
                        first_locator_pattern = r'\s*\(\s*By\.[A-Z_]+\s*,\s*[\'"](.*?)[\'"]\s*\)'
                        
                        for line_idx in range(start_line, j + 1):
                            if re.search(first_locator_pattern, lines[line_idx]):
                                first_locator_line = line_idx
                                break
                        
                        if first_locator_line is not None:
                            current_locator = lines[first_locator_line].strip()
                            print(f"🔍 First locator line ({first_locator_line}): {current_locator}")
                            
                            # Get the best learned locator
                            best_locator = learned_locators[element_name][0]
                            by_type, value = best_locator
                            
                            # Convert by_type to string representation
                            if isinstance(by_type, str):
                                by_str = by_type.upper() if by_type in ['id', 'name', 'class', 'tag', 'css', 'xpath'] else by_type
                            else:
                                by_str = str(by_type).split('.')[-1]
                            
                            # Create the locator string
                            best_locator_str = f"(By.{by_str}, '{value}')"
                            
                            # Debug output
                            print(f"🔍 Current locator: {current_locator}")
                            print(f"🔍 Best locator: {best_locator_str}")
                            
                            # More precise check to see if the locators are different
                            # Extract the current locator's By type and value
                            current_by_match = re.search(r'By\.([A-Z_]+)', current_locator)
                            current_value_match = re.search(r'[\'"]([^\'"]*)[\'"]', current_locator)
                            
                            if current_by_match and current_value_match:
                                current_by = current_by_match.group(1)
                                current_value = current_value_match.group(1)
                                
                                # Compare the actual values, not just string presence
                                if current_by != by_str or current_value != value:
                                    print(f"🔄 Locators are different: {current_by}='{current_value}' vs {by_str}='{value}'")
                                    
                                    # Replace the primary locator with the best learned one
                                    indent = len(lines[first_locator_line]) - len(lines[first_locator_line].lstrip())
                                    new_line = ' ' * indent + best_locator_str + ',  # AI-learned primary locator\n'
                                    lines[first_locator_line] = new_line
                                    
                                    changes_made = True
                                    print(f"📝 UPDATED SOURCE CODE: Primary locator for '{element_name}' is now {best_locator_str}")
                                else:
                                    print(f"🔍 Best locator is already the primary one (same By type and value)")
                            else:
                                print(f"⚠️ Could not parse current locator format: {current_locator}")
                        else:
                            print(f"⚠️ Could not find first locator line for {element_name}")
            
            i += 1
        
        # Write the modified file if changes were made
        if changes_made:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            print(f"✅ Successfully updated source code in {file_path}")
            return True
        else:
            print(f"ℹ️ No locator updates needed in {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error updating source code: {str(e)}")
        traceback.print_exc()
        return False
