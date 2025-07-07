#!/usr/bin/env python3
"""
Auto-restart wrapper for the Telegram bot
This script will automatically restart the bot if it crashes
"""

import subprocess
import time
import sys
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot_runner.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class BotRunner:
    def __init__(self, script_path="main.py", max_restarts=None, restart_delay=10):
        self.script_path = script_path
        self.max_restarts = max_restarts
        self.restart_delay = restart_delay
        self.restart_count = 0
        self.start_time = datetime.now()
        
    def run_bot(self):
        """Run the bot and handle crashes"""
        logger.info(f"🚀 Starting Telegram Bot Runner")
        logger.info(f"Script: {self.script_path}")
        logger.info(f"Max restarts: {self.max_restarts or 'Unlimited'}")
        logger.info(f"Restart delay: {self.restart_delay} seconds")
        
        while True:
            try:
                logger.info(f"📱 Starting bot (attempt #{self.restart_count + 1})")
                
                # Start the bot process
                process = subprocess.Popen(
                    [sys.executable, self.script_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    universal_newlines=True,
                    bufsize=1
                )
                
                # Monitor the process
                while True:
                    output = process.stdout.readline()
                    if output:
                        print(output.strip())
                    
                    # Check if process is still running
                    if process.poll() is not None:
                        break
                        
                # Process has ended
                return_code = process.returncode
                
                if return_code == 0:
                    logger.info("✅ Bot stopped normally")
                    break
                else:
                    logger.error(f"❌ Bot crashed with return code: {return_code}")
                    self.restart_count += 1
                    
                    # Check restart limits
                    if self.max_restarts and self.restart_count >= self.max_restarts:
                        logger.error(f"🚫 Maximum restart limit ({self.max_restarts}) reached")
                        break
                    
                    # Wait before restarting
                    logger.info(f"⏳ Waiting {self.restart_delay} seconds before restart...")
                    time.sleep(self.restart_delay)
                    
            except KeyboardInterrupt:
                logger.info("🛑 Received interrupt signal, stopping bot...")
                if 'process' in locals():
                    process.terminate()
                break
                
            except Exception as e:
                logger.error(f"💥 Unexpected error: {e}")
                self.restart_count += 1
                
                if self.max_restarts and self.restart_count >= self.max_restarts:
                    logger.error(f"🚫 Maximum restart limit ({self.max_restarts}) reached")
                    break
                    
                time.sleep(self.restart_delay)
        
        # Final statistics
        runtime = datetime.now() - self.start_time
        logger.info(f"📊 Bot runner statistics:")
        logger.info(f"   Total runtime: {runtime}")
        logger.info(f"   Total restarts: {self.restart_count}")
        logger.info(f"🏁 Bot runner stopped")

def main():
    # Configuration
    SCRIPT_PATH = "main.py"
    MAX_RESTARTS = None  # Set to None for unlimited restarts
    RESTART_DELAY = 10   # Seconds to wait before restart
    
    # Check if main.py exists
    if not os.path.exists(SCRIPT_PATH):
        logger.error(f"❌ Bot script '{SCRIPT_PATH}' not found!")
        sys.exit(1)
    
    # Create and run the bot runner
    runner = BotRunner(
        script_path=SCRIPT_PATH,
        max_restarts=MAX_RESTARTS,
        restart_delay=RESTART_DELAY
    )
    
    runner.run_bot()

if __name__ == "__main__":
    main()
