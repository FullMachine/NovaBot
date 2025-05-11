import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from bs4 import BeautifulSoup

# Set up Chrome WebDriver
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chromedriver_path = "/opt/homebrew/bin/chromedriver"
    if not os.path.exists(chromedriver_path):
        chromedriver_path = "/usr/local/bin/chromedriver"
        if not os.path.exists(chromedriver_path):
            raise FileNotFoundError("ChromeDriver not found. Please install it via Homebrew or check your path.")
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def scrape_all_nfl_player_slugs():
    url = "https://www.nfl.com/players/"
    all_slugs = set()
    driver = setup_driver()
    print("📥 Scraping NFL.com player slugs...")
    driver.get(url)
    time.sleep(3)

    # Keep clicking 'Show More' until all players are loaded
    while True:
        try:
            show_more = driver.find_element(By.XPATH, '//button[contains(text(), "Show More")]')
            driver.execute_script("arguments[0].scrollIntoView();", show_more)
            time.sleep(0.5)
            show_more.click()
            print("🔄 Clicked 'Show More' to load more players...")
            time.sleep(2)
        except (NoSuchElementException, ElementClickInterceptedException):
            print("✅ All players loaded or no 'Show More' button found.")
            break

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    player_links = soup.select('a[href^="/players/"]')
    found = 0
    for link in player_links:
        href = link.get('href', '')
        # Only keep links like /players/slug/
        parts = href.strip('/').split('/')
        if len(parts) == 2 and parts[0] == 'players':
            slug = parts[1]
            all_slugs.add(slug)
            found += 1
    print(f"✅ Found {found} player links on the page.")
    print(f"✅ Total unique player slugs found: {len(all_slugs)}")
    os.makedirs("players", exist_ok=True)
    with open("players/nfl_players.txt", "w") as f:
        for slug in sorted(all_slugs):
            f.write(slug + "\n")
    print("✅ Saved all player slugs to players/nfl_players.txt")

if __name__ == "__main__":
    scrape_all_nfl_player_slugs() 