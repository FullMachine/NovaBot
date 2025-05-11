import requests
from bs4 import BeautifulSoup

def get_active_years_for_player(player_slug):
    """
    Attempts to pull all valid stat years from the player's main stats page.
    Returns a list of integers representing valid years.
    """
    url = f"https://www.nfl.com/players/{player_slug}/stats/logs/"
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        year_links = soup.select("a.d3-o-tabs__tab")

        years = []
        for link in year_links:
            href = link.get("href", "")
            if "/stats/logs/" in href:
                parts = href.strip("/").split("/")
                if parts[-1].isdigit():
                    years.append(int(parts[-1]))
        return sorted(set(years))
    except Exception as e:
        print(f"⚠️ Failed to get years for {player_slug}: {e}")
        return []