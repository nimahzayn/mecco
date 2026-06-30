from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json

def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")
    options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

def extract_from_url(url: str, driver, wait: int = 3) -> dict:
    """Scrape a (possibly JS-rendered) page."""
    driver.get(url)
    time.sleep(wait)  # let JS render

    soup = BeautifulSoup(driver.page_source, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    text = soup.get_text(separator=" ", strip=True)
    return {
        "text": text,
        "source": url,
        "source_type": "website",
        "title": soup.title.string.strip() if soup.title else ""
    }

def scrape_multiple(urls: list[str]) -> list[dict]:
    driver = get_driver()
    results = []
    for url in urls:
        try:
            print(f"Scraping: {url}")
            data = extract_from_url(url, driver)
            if len(data["text"]) < 50:
                print(f"  ⚠ Very little text — may still need JS or longer wait")
            results.append(data)
        except Exception as e:
            print(f"  Failed: {url} -> {e}")
    driver.quit()
    return results

if __name__ == "__main__":
    urls = [
        "https://ktu.edu.in/Menu/announcements",
        "https://ktu.edu.in/academics/academic_calendar",
        "https://ktu.edu.in/academics/scheme",
        # add more URLs here
    ]

    data = scrape_multiple(urls)
    print(f"\nSuccessfully scraped {len(data)}/{len(urls)} pages")

    with open("web_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Saved to web_data.json")