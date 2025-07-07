#!/usr/bin/env python3
"""
Bot Manager - Helps manage bot conflicts and instances
"""

import requests
import time
import subprocess
import sys
import os

BOT_TOKEN = "7471320098:AAFozaWdh60lXwHRZC4AfwqhsyD13nSZZH0"

def clear_bot_conflicts():
    """Force clear all bot conflicts"""
    try:
        print("🔧 Force clearing bot conflicts...")
        
        # Delete webhook
        webhook_url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook"
        response = requests.post(webhook_url, timeout=10)
        print(f"Webhook clear: {response.status_code}")
        
        # Clear pending updates
        updates_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset=-1"
        response = requests.get(updates_url, timeout=10)
        print(f"Updates clear: {response.status_code}")
        
        # Get bot info to test connection
        info_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
        response = requests.get(info_url, timeout=10)
        if response.status_code == 200:
            bot_info = response.json()
            print(f"✅ Bot ready: @{bot_info['result']['username']}")
        
        time.sleep(3)
        return True
        
    except Exception as e:
        print(f"❌ Error clearing conflicts: {e}")
        return False

def kill_python_processes():
    """Kill all Python processes (use with caution)"""
    try:
        if sys.platform == "win32":
            # Windows
            subprocess.run(["taskkill", "/F", "/IM", "python.exe"], 
                         capture_output=True, text=True)
            print("✅ Killed Windows Python processes")
        else:
            # Linux/Mac
            subprocess.run(["pkill", "-f", "python"], 
                         capture_output=True, text=True)
            print("✅ Killed Unix Python processes")
        
        time.sleep(2)
        return True
        
    except Exception as e:
        print(f"❌ Error killing processes: {e}")
        return False

def start_bot():
    """Start the bot with conflict resolution"""
    print("🚀 Starting bot...")
    try:
        subprocess.run([sys.executable, "main.py"], cwd=os.getcwd())
    except KeyboardInterrupt:
        print("\n⏹️ Bot stopped by user")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")

def main():
    print("🤖 Bot Manager")
    print("=" * 40)
    
    while True:
        print("\nOptions:")
        print("1. Clear bot conflicts")
        print("2. Kill all Python processes (CAUTION)")
        print("3. Start bot")
        print("4. Clear conflicts + Start bot")
        print("5. Exit")
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == "1":
            clear_bot_conflicts()
            
        elif choice == "2":
            confirm = input("⚠️ This will kill ALL Python processes. Continue? (y/N): ")
            if confirm.lower() == 'y':
                kill_python_processes()
            else:
                print("❌ Cancelled")
                
        elif choice == "3":
            start_bot()
            
        elif choice == "4":
            if clear_bot_conflicts():
                print("✅ Conflicts cleared, starting bot...")
                start_bot()
            else:
                print("❌ Failed to clear conflicts")
                
        elif choice == "5":
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()
