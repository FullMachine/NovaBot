import os
import polars as pl
from utils.sources.api_scraper import MLB_Scrape

def fetch_mlb_players():
    print("⚾️ Fetching MLB players using mlb_scraper...")

    try:
        scraper = MLB_Scrape()
        df = scraper.get_players(sport_id=1, season="2024")  # You can change season later

        # Extract and format player names
        player_names = df.select(
            (pl.col("first_name") + " " + pl.col("last_name")).alias("full_name")
        ).to_series().to_list()

        # Save to file
        output_file = "players/mlb_players.txt"
        with open(output_file, "w") as f:
            for name in sorted(set(player_names)):
                f.write(name.lower() + "\n")

        print(f"✅ Saved {len(player_names)} MLB players to {output_file}")
    
    except Exception as e:
        print(f"❌ Error fetching MLB players: {e}")

if __name__ == "__main__":
    fetch_mlb_players()