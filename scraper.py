import requests
from bs4 import BeautifulSoup
import os

BASE_URL = "https://chachaboylogistics.com/"
OUTPUT_FILE = "business_info.txt"

def scrape_website(url):
    try:
        print(f"Scraping {url} ...")
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        text = soup.get_text(separator="\n", strip=True)
        return text
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return ""

def update_business_info():
    # You can expand this list with key pages
    pages = [
        BASE_URL,
        f"{BASE_URL}/services",
        f"{BASE_URL}/contact-us",
        f"{BASE_URL}/about-us", 
        f"{BASE_URL}/customs-policies/",
        f"{BASE_URL}/rates/",
    ]

    content = ""
    for page in pages:
        content += scrape_website(page) + "\n\n"

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(content[:10000])  # Limit to first 10,000 chars

    print("✅ Business info updated successfully!")

if __name__ == "__main__":
    update_business_info()
