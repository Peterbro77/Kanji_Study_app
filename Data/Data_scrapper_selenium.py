import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Output CSV path
output_csv = r"C:/Users/peter/Desktop/Peter/study stuff/DS/Kanji_Study_app/Kanji_Data/N2_Kanji4.csv"

# Set up Selenium with headless Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--log-level=3")  # Suppress logs

# Update path to your ChromeDriver executable
driver_path = "C:/Users/peter/Desktop/Peter/study stuff/DS/Kanji_Study_app/Kanji_Data/chromedriver.exe"  # ⬅ Change this to your chromedriver path

driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)

# URL to scrape
url = "https://jlptsensei.com/jlpt-n2-kanji-list/page/4/"
driver.get(url)
time.sleep(3)  # Wait for content to load

# Parse page with BeautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

# Extract data
kanji_rows = soup.select("table tr")[1:]  # Skip header
data = []

for row in kanji_rows:
    cols = row.find_all("td")
    if len(cols) >= 5:
        sno = cols[0].text.strip()
        Kanji = cols[1].text.strip()
        Onyomi = cols[2].text.strip()
        Kunyomi = cols[3].text.strip()
        Meaning = cols[4].text.strip()
        
        data.append({
            "sno": sno,
            "Kanji": Kanji,
            "Onyomi": Onyomi,
            "Kunyomi": Kunyomi,
            "Meaning": Meaning,
            
        })

# Save to CSV
df = pd.DataFrame(data)
df.to_csv(output_csv, index=False, encoding="utf-8-sig")

print(f"✅ Scraped {len(df)} kanji and saved to {output_csv}")
