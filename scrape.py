from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os
from datetime import datetime

def scrape_second_table_to_json(url, output_file='scraped_data.json'):
    # Setup Chrome driver
    driver = webdriver.Chrome()
    try:
        # Navigate to the webpage
        print("Navigating to the webpage...")
        driver.get(url)
        
        # Wait for tables to be present and get the second table
        print("Locating tables...")
        tables = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "table"))
        )
        
        if len(tables) < 2:
            raise Exception("Less than 2 tables found on the page")
            
        table = tables[1]  # Get the second table
        print("Second table found successfully!")
        
        # Get headers
        headers = []
        header_cells = table.find_elements(By.CSS_SELECTOR, "tr:first-child td")
        for cell in header_cells:
            headers.append(cell.text.strip())
        
        print(f"Found {len(headers)} columns: {', '.join(headers)}")
        
        # Get data rows
        data = []
        rows = table.find_elements(By.TAG_NAME, "tr")[1:]  # Skip header row
        
        print(f"Processing {len(rows)} rows...")
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            row_data = {}
            for header, cell in zip(headers, cells):
                row_data[header] = cell.text.strip()
            data.append(row_data)
        
        # Create a directory for the output if it doesn't exist
        output_dir = 'scraped_data'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # Add timestamp to filename to avoid overwriting
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{output_dir}/{os.path.splitext(output_file)[0]}_{timestamp}.json"
        
        # Save to JSON file with proper formatting
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        print(f"\nData successfully scraped and saved to: {filename}")
        print(f"Total records saved: {len(data)}")
        
        # Return the data and filename for further use if needed
        return data, filename
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None, None
    finally:
        driver.quit()

def display_sample_data(filename):
    """Display sample data from the saved JSON file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print("\nFirst 2 records from the saved data:")
            print(json.dumps(data[:2], indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error reading the saved file: {str(e)}")

# Example usage:
if __name__ == "__main__":
    # Replace with your actual URL
    url = "https://sih.gov.in/screeningresult"
    
    # Scrape the data
    scraped_data, output_file = scrape_second_table_to_json(url)
    
    if scraped_data and output_file:
        # Display sample of saved data
        display_sample_data(output_file)