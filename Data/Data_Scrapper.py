import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://jlptsensei.com/jlpt-n3-kanji-list/page/2/"  # Replace with actual N3 kanji list URL
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Locate the correct table on the page
table = soup.find("table")  # Adjust if needed based on structure
rows = table.find_all("tr")

data = []
for row in rows[1:]:  # Skip header row
    cols = row.find_all("td")
    if len(cols) >= 5:
        kanji = cols[1].text.strip()
        onyomi = cols[2].text.strip()
        kunyomi = cols[3].text.strip()
        meaning = cols[4].text.strip()
        data.append({
            "Kanji": kanji,
            "Onyomi": onyomi,
            "Kunyomi": kunyomi,
            "Meaning": meaning
        })

# Save as CSV
df = pd.DataFrame(data)
df.to_csv("C:/Users/peter/Desktop/Peter/study stuff/DS/Kanji_Study_app/Kanji_Data/Kanji_data_new.csv", index=False, encoding='utf-8-sig')
print("✅ Kanji Master data scraped and saved!")
