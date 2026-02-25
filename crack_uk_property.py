from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
import time

# Setup Chrome Options
chrome_options = Options()

# Google chrome is needed to run this scraper!
chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# chrome_options.add_argument("--headless") # Run without a window showing
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# Initialize the Robot
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options) #type: ignore

try:
    url = "https://manningstainton.co.uk/properties-for-sale/leeds"
    print(f"🚀 Launching browser to: {url}")
    driver.get(url)

    # CLICK THE COOKIE BANNER (The "Accept All" button)
    print("🍪 Attempting to clear cookie banner...")
    try:
        # This looks for the red button you see in the screenshot
        wait = WebDriverWait(driver, 10)
        accept_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'ACCEPT ALL')]")))
        accept_btn.click()
        #print("✅ Cookies accepted! Page cleared.")
        time.sleep(2) # Let the banner fade out
    except Exception as e:
        print(f"ℹ️ Could not click cookie button, might be blocked: {e}")

    # WAIT AND SCROLL
    time.sleep(5) 
    driver.execute_script("window.scrollTo(0, 500);")
    time.sleep(2)

    # GRAB AND PARSE
    soup = BeautifulSoup(driver.page_source, 'lxml')
    
    # Based on screenshot, target the text directly
    results = []
    
    # Find all property containers
    # In screenshot, houses have titles like 'Church Gate' and prices next to them
    properties = soup.find_all('div', class_='property-res') or soup.find_all('div', class_='property-item')
    
    if not properties:
        #print("🔍 Searching for headers and prices by text...")
        # Fallback: Find every H3 (titles) and look for prices nearby
        for h3 in soup.find_all('h3'):
            title = h3.get_text(strip=True)
            # Find the price in the parent container
            parent = h3.find_parent('div')
            price_elem = (
                parent.find(string=lambda s: '£' in str(s)) if parent else None)
            
            # Only proceed if price and title weere successfully extracted.
            if title and price_elem:
                results.append({
                    "title": title, # Store the title
                    "price": price_elem.strip() # Strip whitespace and store the price.
                })
    else:
        for p in properties:
            # These are the specific classes Manning Stainton uses
            title = (
                p.find(['h2', 'h3']).get_text(strip=True) #type:ignore
                if p.find(['h2', 'h3']) 
                else "N/A")
            
            price = (
                p.find(class_='price').get_text(strip=True) #type:ignore
                if p.find(class_='price') 
                else "N/A")
            
            results.append({"title": title, "price": price})

    print(f"✅ Success! Found {len(results)} properties.")

    # SAVE
    with open('selenium_leeds_results.json', 'w') as f:
        json.dump(results, f, indent=4)
    #print("📂 Data saved to selenium_leeds_results.json")

finally:
    time.sleep(5) # Wait a little for the website to load.
    driver.quit()