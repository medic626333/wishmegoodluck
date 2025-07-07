#!/usr/bin/env python3
"""
Health check script for the Telegram bot
This script monitors the bot's health and can restart it if needed
"""

import requests
import time
import subprocess
import sys
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('health_check.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class BotHealthChecker:
    def __init__(self, bot_token, check_interval=300):
        self.bot_token = bot_token
        self.check_interval = check_interval  # 5 minutes default
        self.api_url = f"https://api.telegram.org/bot{bot_token}"
        
    def check_bot_status(self):
        """Check if bot is responding to Telegram API"""
        try:
            response = requests.get(f"{self.api_url}/getMe", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('ok'):
                    logger.info("✅ Bot is responding to API calls")
                    return True
                else:
                    logger.error(f"❌ Bot API returned error: {data}")
                    return False
            else:
                logger.error(f"❌ Bot API returned status code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Failed to connect to Telegram API: {e}")
            return False
    
    def check_service_status(self):
        """Check if systemd service is running"""
        try:
            result = subprocess.run(
                ['systemctl', 'is-active', 'telegram-bot.service'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0 and result.stdout.strip() == 'active':
                logger.info("✅ Systemd service is active")
                return True
            else:
                logger.error(f"❌ Systemd service is not active: {result.stdout.strip()}")
                return False
        except Exception as e:
            logger.error(f"❌ Failed to check service status: {e}")
            return False
    
    def restart_service(self):
        """Restart the bot service"""
        try:
            logger.info("🔄 Attempting to restart bot service...")
            result = subprocess.run(
                ['sudo', 'systemctl', 'restart', 'telegram-bot.service'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                logger.info("✅ Service restarted successfully")
                return True
            else:
                logger.error(f"❌ Failed to restart service: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"❌ Exception while restarting service: {e}")
            return False
    
    def send_alert(self, message):
        """Send alert message to owner (optional)"""
        try:
            owner_id = "1172862169"  # Replace with your owner ID
            url = f"{self.api_url}/sendMessage"
            data = {
                'chat_id': owner_id,
                'text': f"🚨 Bot Health Alert 🚨\n\n{message}\n\nTime: {datetime.now()}",
                'parse_mode': 'HTML'
            }
            response = requests.post(url, data=data, timeout=10)
            if response.status_code == 200:
                logger.info("📱 Alert sent to owner")
            else:
                logger.error(f"❌ Failed to send alert: {response.status_code}")
        except Exception as e:
            logger.error(f"❌ Failed to send alert: {e}")
    
    def run_health_check(self):
        """Run a single health check"""
        logger.info("🔍 Running health check...")
        
        # Check service status
        service_ok = self.check_service_status()
        
        # Check API status
        api_ok = self.check_bot_status()
        
        if not service_ok or not api_ok:
            logger.warning("⚠️ Health check failed, attempting restart...")
            
            # Try to restart the service
            if self.restart_service():
                # Wait a bit and check again
                time.sleep(30)
                if self.check_service_status() and self.check_bot_status():
                    logger.info("✅ Service restarted successfully and is healthy")
                    self.send_alert("Bot was restarted due to health check failure but is now running normally.")
                else:
                    logger.error("❌ Service restart failed or bot still unhealthy")
                    self.send_alert("CRITICAL: Bot restart failed! Manual intervention required.")
            else:
                logger.error("❌ Failed to restart service")
                self.send_alert("CRITICAL: Failed to restart bot service! Manual intervention required.")
        else:
            logger.info("✅ All health checks passed")
    
    def run_continuous_monitoring(self):
        """Run continuous health monitoring"""
        logger.info(f"🔄 Starting continuous health monitoring (interval: {self.check_interval}s)")
        
        while True:
            try:
                self.run_health_check()
                logger.info(f"⏰ Next check in {self.check_interval} seconds...")
                time.sleep(self.check_interval)
            except KeyboardInterrupt:
                logger.info("🛑 Health monitoring stopped by user")
                break
            except Exception as e:
                logger.error(f"❌ Unexpected error in health monitoring: {e}")
                time.sleep(60)  # Wait a minute before retrying

def main():
    # Configuration
    BOT_TOKEN = "7471320098:AAFozaWdh60lXwHRZC4AfwqhsyD13nSZZH0"  # Replace with your bot token
    CHECK_INTERVAL = 300  # 5 minutes
    
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        # Run single health check
        checker = BotHealthChecker(BOT_TOKEN, CHECK_INTERVAL)
        checker.run_health_check()
    else:
        # Run continuous monitoring
        checker = BotHealthChecker(BOT_TOKEN, CHECK_INTERVAL)
        checker.run_continuous_monitoring()

if __name__ == "__main__":
    main()
