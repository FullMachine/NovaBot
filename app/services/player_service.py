import os
import openai
from dotenv import load_dotenv

load_dotenv()

class PlayerService:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.openai_api_key

    def get_players(self, sport="nba"):
        """Load player names for a sport"""
        try:
            with open(f"data/players/{sport}_players.txt", "r") as f:
                return [line.strip().lower() for line in f.readlines()]
        except FileNotFoundError:
            return []

    def save_player(self, name, sport="nba"):
        """Save new player to file"""
        name = name.strip().lower()
        if not name:
            return
        
        players = self.get_players(sport)
        if name not in players:
            with open(f"data/players/{sport}_players.txt", "a") as f:
                f.write(name + "\n")

    def is_valid_player(self, name, sport="nba"):
        """Verify if a player name is valid using GPT"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": f"You're a sports assistant. Confirm only real {sport.upper()} player names (past, present, or future)."
                    },
                    {
                        "role": "user",
                        "content": f"Is '{name}' a real {sport.upper()} player? Just say YES or NO."
                    }
                ],
                temperature=0.2
            )
            reply = response['choices'][0]['message']['content'].strip().lower()
            return "yes" in reply
        except Exception as e:
            print("[GPT ERROR]", e)
            return False 