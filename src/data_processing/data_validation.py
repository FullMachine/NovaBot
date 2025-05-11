import json
import logging
from pathlib import Path
from typing import Dict, List, Any
import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_validation.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class NBADataValidator:
    def __init__(self, data_dir: str = 'data/nba'):
        self.data_dir = Path(data_dir)
        self.required_fields = {
            'info': ['name', 'position', 'height', 'weight', 'birth_date', 'college'],
            'career_stats': [],
            'season_stats': []
        }
        
    def validate_player_data(self, player_id: str) -> Dict[str, Any]:
        """Validate data for a specific player."""
        player_file = self.data_dir / f"{player_id}.json"
        if not player_file.exists():
            return {"valid": False, "errors": [f"Player file {player_id}.json not found"]}
            
        try:
            with open(player_file, 'r') as f:
                player_data = json.load(f)
        except json.JSONDecodeError as e:
            return {"valid": False, "errors": [f"Invalid JSON format: {str(e)}"]}
            
        errors = []
        
        # Check required sections
        for section in self.required_fields.keys():
            if section not in player_data:
                errors.append(f"Missing section: {section}")
                continue
                
            # Check required fields in info section
            if section == 'info':
                for field in self.required_fields[section]:
                    if field not in player_data[section]:
                        errors.append(f"Missing field {field} in info section")
                        
        # Validate data types
        if 'info' in player_data:
            info = player_data['info']
            if not isinstance(info.get('name', ''), str):
                errors.append("Invalid type for name field")
            if not isinstance(info.get('position', ''), str):
                errors.append("Invalid type for position field")
            if not isinstance(info.get('height', ''), str):
                errors.append("Invalid type for height field")
            if not isinstance(info.get('weight', ''), str):
                errors.append("Invalid type for weight field")
            if not isinstance(info.get('birth_date', ''), str):
                errors.append("Invalid type for birth_date field")
            if not isinstance(info.get('college', ''), str):
                errors.append("Invalid type for college field")
                
        # Validate career_stats and season_stats
        if not isinstance(player_data.get('career_stats', {}), dict):
            errors.append("Invalid type for career_stats")
        if not isinstance(player_data.get('season_stats', []), list):
            errors.append("Invalid type for season_stats")
            
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "player_id": player_id
        }
        
    def validate_all_players(self) -> Dict[str, Any]:
        """Validate data for all players in the data directory."""
        results = {
            "total_players": 0,
            "valid_players": 0,
            "invalid_players": 0,
            "player_results": []
        }
        
        for player_file in self.data_dir.glob("*.json"):
            player_id = player_file.stem
            validation_result = self.validate_player_data(player_id)
            results["player_results"].append(validation_result)
            results["total_players"] += 1
            
            if validation_result["valid"]:
                results["valid_players"] += 1
            else:
                results["invalid_players"] += 1
                
        return results
        
    def generate_validation_report(self, results: Dict[str, Any]) -> None:
        """Generate a detailed validation report."""
        report_file = self.data_dir / "validation_report.json"
        
        with open(report_file, 'w') as f:
            json.dump(results, f, indent=2)
            
        logger.info(f"Validation report saved to {report_file}")
        logger.info(f"Total players: {results['total_players']}")
        logger.info(f"Valid players: {results['valid_players']}")
        logger.info(f"Invalid players: {results['invalid_players']}")
        
        if results['invalid_players'] > 0:
            logger.warning("Some players have invalid data. Check validation_report.json for details.")

def main():
    validator = NBADataValidator()
    results = validator.validate_all_players()
    validator.generate_validation_report(results)

if __name__ == "__main__":
    main() 