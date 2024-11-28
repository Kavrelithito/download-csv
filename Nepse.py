
#this is very tough Test
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date

# Define custom download directory
download_dir = "/tmp"
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Chrome options
options = Options()
options.add_argument("--headless")  # Enable headless mode
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.78 Safari/537.36"
)

# Add download preferences
prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "safebrowsing.enabled": True
}
options.add_experimental_option("prefs", prefs)

# ChromeDriver path
driver_path = os.path.join(os.path.dirname(__file__), "drivers", "chromedriver")
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

try:
    # Open the target URL
    driver.get("https://www.nepalstock.com/today-price")
    print("Page title:", driver.title)

    # Wait for the page to fully load
    WebDriverWait(driver, 30).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

    # Save the page source for debugging
    with open("headless_page_source.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print("Page source saved for inspection.")

    # Locate and interact with the CSV download button
    try:
        csv_download_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Download as CSV')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", csv_download_button)
        csv_download_button.click()
        print("CSV download initiated.")
    except Exception as e:
        print("Button not interactable, trying JavaScript.")
        # Try JavaScript fallback
        driver.execute_script("document.querySelector('a[href*=\"export\"]').click();")

    # Wait for the download to complete
    time.sleep(5)

    # Verify download
    today_date = date.today().strftime('%Y-%m-%d')
    downloaded_file = os.path.join(download_dir, f"Today's Price - {today_date}.csv")
    if os.path.exists(downloaded_file):
        print(f"File downloaded successfully: {downloaded_file}")
    else:
        print(f"File not found in {download_dir}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()