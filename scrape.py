from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os
from datetime import datetime

def scrape_second_table_to_json(url, output_file='scraped_data.json'):
    driver = webdriver.Chrome()
    try:
        print("Navigating to the webpage...")
        driver.get(url)
        
        print("Locating tables...")
        tables = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "table"))
        )
        
        if len(tables) < 2:
            raise Exception("Less than 2 tables found on the page")
            
        table = tables[1]  # Get the second table
        print("Second table found successfully!")
        
        headers = []
        header_cells = table.find_elements(By.CSS_SELECTOR, "tr:first-child td")
        for cell in header_cells:
            headers.append(cell.text.strip())
        
        print(f"Found {len(headers)} columns: {', '.join(headers)}")
        
        data = []
        rows = table.find_elements(By.TAG_NAME, "tr")[1:]  # Skip header row
        
        print(f"Processing {len(rows)} rows...")
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            row_data = {}
            for header, cell in zip(headers, cells):
                row_data[header] = cell.text.strip()
            data.append(row_data)
        
        output_dir = 'scraped_data'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{output_dir}/{os.path.splitext(output_file)[0]}_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        print(f"\nData successfully scraped and saved to: {filename}")
        print(f"Total records saved: {len(data)}")
        
        return data, filename
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None, None
    finally:
        driver.quit()

def display_sample_data(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print("\nFirst 2 records from the saved data:")
            print(json.dumps(data[:2], indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error reading the saved file: {str(e)}")

if __name__ == "__main__":
    url = "https://sih.gov.in/screeningresult"
    
    scraped_data, output_file = scrape_second_table_to_json(url)
    
    if scraped_data and output_file:
        display_sample_data(output_file)