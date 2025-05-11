from PIL import Image
import pytesseract
from app.services.player_service import PlayerService
import os

class OCRService:
    def __init__(self):
        self.player_service = PlayerService()

    def process_screenshot(self, file, sport="nba"):
        """Process a screenshot and detect players"""
        image = Image.open(file.stream)
        raw_text = pytesseract.image_to_string(image)
        words = raw_text.split('\n')
        tried_names = [w.strip() for w in words if w.strip()]

        detected = []
        for name in tried_names:
            name_clean = name.lower().strip()
            if self.player_service.is_valid_player(name_clean, sport):
                detected.append(name.title())
                self.player_service.save_player(name_clean, sport)

        if not detected:
            return {
                "error": "No players found or valid stats fetched",
                "tried_names": tried_names
            }

        return {
            "players_detected": detected,
            "total_detected": len(detected),
            "tried_names": tried_names
        } 