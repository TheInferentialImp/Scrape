import csv
import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

# --- Scraper Logic for SignalHire ---
def signalhire_scraper():
    profile_path = "/Users/onyx/Library/Application Support/Google/Chrome/User Data"  # Correct path for macOS
    profile_name = "Alex"  # Or "Default" or another profile name
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument(f"--user-data-dir={profile_path}")
    options.add_argument(f"--profile-directory={profile_name}")
    
    # Keep headless off for visibility during testing
    options.headless = False  # Use headless mode as False for debugging
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--no-sandbox")
    
    driver = uc.Chrome(options=options)
    all_data = []

    def scrape_page(page_number):
        url = f"https://www.signalhire.com/companies/alliance-behavioral-healthcare/employees?page={page_number}"
        driver.get(url)

        time.sleep(random.uniform(3, 5))

        # Check if redirected to login page
        if "login" in driver.current_url.lower():
            print(f"Redirected to login on page {page_number}")
            return []

        names, positions = [], []
        name_elements = driver.find_elements(By.CSS_SELECTOR, 'div[data-candidate-name]')
        position_elements = driver.find_elements(By.CSS_SELECTOR, 'div.col-lg-3.col-12.mt-1.text-truncate small.fw-normal')

        for name_el, pos_el in zip(name_elements, position_elements):
            name = name_el.get_attribute("data-candidate-name")
            position = pos_el.text.strip()

            if name and position:
                names.append(name)
                positions.append(position)

        return list(zip(names, positions))

    # Scrape 4 pages (adjust the range as needed)
    for i in range(1, 5):
        try:
            print(f"Scraping page {i}...")
            results = scrape_page(i)
            all_data.extend(results)
            print(f"Page {i}: {len(results)} entries collected.")
            time.sleep(random.uniform(2, 4))
        except Exception as e:
            print(f"Error on page {i}: {e}")
            time.sleep(random.uniform(3, 6))

    driver.quit()
    return [{"name": name, "position": position} for name, position in all_data]

# --- Write to CSV ---
if __name__ == '__main__':
    scraped_data = signalhire_scraper()
    if scraped_data:
        keys = scraped_data[0].keys()
        with open("signalhire_employees.csv", "w", newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(scraped_data)
        print(f"\n✅ Data written to signalhire_employees.csv ({len(scraped_data)} entries)")
    else:
        print("\n⚠️ No data scraped.")
