import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

teams = {
    "ATLANTA HAWKS": "1610612737",
    "BOSTON CELTICS": "1610612738",
    "BROOKLYN NETS": "1610612751",
    "CHARLOTTE HORNETS": "1610612766",
    "CHICAGO BULLS": "1610612741",
    "CLEVELAND CAVALIERS": "1610612739",
    "DALLAS MAVERICKS": "1610612742",
    "DENVER NUGGETS": "1610612743",
    "DETROIT PISTONS": "1610612765",
    "GOLDEN STATE WARRIORS": "1610612744",
    "HOUSTON ROCKETS": "1610612745",
    "INDIANA PACERS": "1610612754",
    "LOS ANGELES CLIPPERS": "1610612746",
    "LOS ANGELES LAKERS": "1610612747",
    "MEMPHIS GRIZZLIES": "1610612763",
    "MIAMI HEAT": "1610612748",
    "MILWAUKEE BUCKS": "1610612749",
    "MINNESOTA TIMBERWOLVES": "1610612750",
    "NEW ORLEANS PELICANS": "1610612740",
    "NEW YORK KNICKS": "1610612752",
    "OKLAHOMA CITY THUNDER": "1610612760",
    "ORLANDO MAGIC": "1610612753",
    "PHILADELPHIA 76ERS": "1610612755",
    "PHOENIX SUNS": "1610612756",
    "PORTLAND TRAIL BLAZERS": "1610612757",
    "SACRAMENTO KINGS": "1610612758",
    "SAN ANTONIO SPURS": "1610612759",
    "TORONTO RAPTORS": "1610612761",
    "UTAH JAZZ": "1610612762",
    "WASHINGTON WIZARDS": "1610612764"
}

def fetch_active_nba_players():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    all_players = []

    for team, team_id in teams.items():
        url = f"https://www.nba.com/team/{team_id}/{team.lower().replace(' ', '-')}/roster"
        print(f"🔍 Scraping {team} from {url}")
        try:
            driver.get(url)
            time.sleep(5)  # let page load

            links = driver.find_elements(By.CSS_SELECTOR, "a.Anchor_anchor__cSc3P")
            player_names = [link.text.strip() for link in links if "/player/" in link.get_attribute("href")]

            if player_names:
                for name in player_names:
                    player_id = name.lower().replace(" ", "-")
                    all_players.append(player_id)
            else:
                print(f"❌ No players found on {team}")
        except Exception as e:
            print(f"❌ Error on {team}: {e}")

    driver.quit()

    with open("players/nba_players.txt", "w") as f:
        for player in sorted(set(all_players)):
            f.write(player + "\n")

    print(f"✅ Saved {len(all_players)} NBA players to players/nba_players.txt")

if __name__ == "__main__":
    fetch_active_nba_players()