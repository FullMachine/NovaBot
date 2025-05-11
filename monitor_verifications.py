import json
import os
from datetime import datetime, timedelta
import logging
from typing import List, Dict
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('verification_monitor.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class VerificationMonitor:
    def __init__(self, data_dir: str = 'data/nba'):
        self.data_dir = data_dir
        self.verification_files = []
        self.issues = []
        
    def load_verification_files(self) -> List[str]:
        """Load all verification files from the data directory"""
        self.verification_files = [
            f for f in os.listdir(self.data_dir) 
            if f.startswith('verification_') and f.endswith('.json')
        ]
        return self.verification_files
        
    def analyze_verifications(self) -> List[Dict]:
        """Analyze verification results and identify issues"""
        self.issues = []
        
        for file in self.verification_files:
            try:
                with open(os.path.join(self.data_dir, file), 'r') as f:
                    result = json.load(f)
                    
                # Check for errors
                if 'error' in result:
                    self.issues.append({
                        'type': 'error',
                        'player_id': result['player_id'],
                        'message': result['error'],
                        'timestamp': result['verification_time']
                    })
                
                # Check for mismatches
                elif not result['matches']:
                    self.issues.append({
                        'type': 'mismatch',
                        'player_id': result['player_id'],
                        'player_name': result['player_name'],
                        'our_games': result['our_games'],
                        'official_games': result['official_games'],
                        'timestamp': result['verification_time']
                    })
                    
            except Exception as e:
                logger.error(f"Error analyzing {file}: {str(e)}")
                
        return self.issues
        
    def generate_report(self) -> str:
        """Generate a human-readable report of verification issues"""
        if not self.issues:
            return "No verification issues found."
            
        report = ["Verification Issues Report:", "=" * 30, ""]
        
        for issue in self.issues:
            if issue['type'] == 'error':
                report.append(f"Error for player {issue['player_id']}:")
                report.append(f"  - {issue['message']}")
                report.append(f"  - Time: {issue['timestamp']}")
            else:
                report.append(f"Mismatch for {issue['player_name']} (ID: {issue['player_id']}):")
                report.append(f"  - Our games: {issue['our_games']}")
                report.append(f"  - Official games: {issue['official_games']}")
                report.append(f"  - Time: {issue['timestamp']}")
            report.append("")
            
        return "\n".join(report)
        
    def send_alert(self, report: str, email_config: Dict):
        """Send an email alert with the verification report"""
        try:
            msg = MIMEMultipart()
            msg['From'] = email_config['from_email']
            msg['To'] = email_config['to_email']
            msg['Subject'] = "NBA Data Verification Alert"
            
            msg.attach(MIMEText(report, 'plain'))
            
            with smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port']) as server:
                server.starttls()
                server.login(email_config['username'], email_config['password'])
                server.send_message(msg)
                
            logger.info("Alert email sent successfully")
        except Exception as e:
            logger.error(f"Error sending alert email: {str(e)}")

def main():
    monitor = VerificationMonitor()
    
    # Load and analyze verifications
    monitor.load_verification_files()
    issues = monitor.analyze_verifications()
    
    # Generate and log report
    report = monitor.generate_report()
    logger.info("\n" + report)
    
    # If there are issues, send an alert
    if issues:
        # Configure email settings (you'll need to fill these in)
        email_config = {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'username': 'your-email@gmail.com',
            'password': 'your-app-password',
            'from_email': 'your-email@gmail.com',
            'to_email': 'recipient@example.com'
        }
        
        monitor.send_alert(report, email_config)

if __name__ == "__main__":
    main() 