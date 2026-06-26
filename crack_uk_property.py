from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv

# Setup Chrome Options
chrome_options = Options()

# Google chrome is needed to run this scraper!
chrome_options.binary_location = (
    r"C:\Program Files\Google\Chrome\Application\chrome.exe"
)

# chrome_options.add_argument("--headless") # Run without a window showing
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

# Initialize the Robot
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    url = "https://manningstainton.co.uk/properties-for-sale/leeds"
    print(f"🚀 Launching browser to: {url}")
    driver.get(url)

    # CLICK THE COOKIE BANNER (The "Accept All" button)
    print("🍪 Attempting to clear cookie banner...")
    try:
        wait = WebDriverWait(driver, 5)
        accept_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'ACCEPT ALL')]")
            )
        )
        accept_btn.click()
        print("✅ Cookies accepted! Page cleared.")
        time.sleep(2)  # Let the banner fade out
    except Exception:
        print("ℹ️ Could not click cookie button, might be blocked or already cleared.")

    # WAIT AND SCROLL
    print("⏳ Waiting for listings to load and scrolling down...")
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, 800);")
    time.sleep(3)

    # Parse the current page source using BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "lxml")

    results = []
    seen_properties = set()

    print("🔍 Parsing page data using smart card-hunting extraction...")

    # 💡 UPGRADED CARD-HUNTING LOGIC
    # We find layout elements containing BOTH a price symbol and a West Yorkshire 
    # region marker, while strictly avoiding filter dropdowns, forms, or navigation panels.
    possible_cards = []
    for candidate in soup.find_all(["div", "article", "li"]):
        # Hard ignore structural frames, search bars, side filters, and menus
        if candidate.find_parent(["form", "select", "option", "nav", "footer", "header", "script", "style"]):
            continue
        
        text = candidate.get_text(separator=" ", strip=True)
        # A valid property listing must show a price and look like a local address
        if "£" in text and any(marker in text.upper() for marker in ["LEEDS", "PUDSEY", "MORLEY", "WORTLEY", "HORSFORTH", "LS", "WF", "BD"]):
            possible_cards.append(candidate)

    # Filter out overarching macro-containers to zero in on the precise listing cards
    cards = []
    for c in possible_cards:
        has_child_card = False
        for other in possible_cards:
            if other is not c and other in c.descendants:
                has_child_card = True
                break
        if not has_child_card:
            cards.append(c)

    # Extract clean information out of our matched property card boxes
    for card in cards:
        strings = [s.strip() for s in card.stripped_strings if s.strip()]
        
        # 1. Isolate the true listing price element
        price_str = "N/A"
        for s in strings:
            if "£" in s and len(s) <= 15:
                price_str = s
                break
                
        # 2. Isolate the longest descriptive regional address line
        location_candidates = []
        for s in strings:
            if any(marker in s.upper() for marker in ["LEEDS", "PUDSEY", "MORLEY", "WORTLEY", "HORSFORTH", "LS", "WF", "BD"]):
                if "£" not in s and len(s) > 4 and "VIEW" not in s.upper() and "PROPERTY" not in s.upper():
                    location_candidates.append(s)
                    
        if location_candidates:
            # Grabbing the longest string ensures we get the full address line instead of an excerpt
            location_str = max(location_candidates, key=len)
        else:
            # Safe text fallback array
            non_price_strings = [s for s in strings if "£" not in s and len(s) > 4 and "PRICE" not in s.upper() and "VIEW" not in s.upper()]
            location_str = non_price_strings[0] if non_price_strings else "N/A"

        if price_str != "N/A" and location_str != "N/A":
            # Fix duplicate string-stitching layers if elements double-rendered inside the HTML
            half = len(location_str) // 2
            if len(location_str) >= 4 and location_str[:half] == location_str[half:]:
                location_str = location_str[:half]
                
            location_str = location_str.strip(". ,")
            
            # Deduplicate rows
            prop_id = f"{location_str}-{price_str}"
            if prop_id not in seen_properties:
                results.append({"title": location_str, "price": price_str})
                seen_properties.add(prop_id)

    print(f"✅ Success! Found {len(results)} clean, valid property listings.")

    # Save report to a CSV file
    csv_file = "leeds_properties.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Property ID", "Location or Title", "Price"])

        for index, prop in enumerate(results, 1):
            writer.writerow([f"Property {index:02d}", prop["title"], prop["price"]])

    print(f"CSV file generated successfully: {csv_file}")

finally:
    time.sleep(5)
    driver.quit()