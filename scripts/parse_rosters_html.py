# scripts/parse_rosters_html.py

from lxml import html
import os

# Path to the downloaded HTML file
html_file = "nflscraper-data/data/rosters_2023.html"

# Output file for player names
output_file = "players/nfl_players.txt"

# Load HTML
with open(html_file, "r", encoding="utf-8") as f:
    tree = html.fromstring(f.read())

# Extract player names using XPath
# This may change depending on the website structure
# Let's try a generic pattern for now:
player_names = tree.xpath('//a[contains(@href, "/players/")]/text()')

# Clean up duplicates and whitespace
cleaned = sorted(set([name.strip() for name in player_names if name.strip()]))

# Save to file
with open(output_file, "w") as f:
    for name in cleaned:
        f.write(name + "\n")

print(f"✅ Extracted {len(cleaned)} players to {output_file}")