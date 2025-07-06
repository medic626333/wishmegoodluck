import requests

def get_chat_id():
    print("🔍 Chat ID Finder")
    print("=" * 30)
    
    # Your bot token
    token = "7893259724:AAFfxQ5TuhiHtv9hr6QGBg524d0p-vaFGaI"
    
    print("📋 Instructions:")
    print("1. Add your bot to any group/channel")
    print("2. Send any message in that group/channel")
    print("3. Run this script to get the chat ID")
    print()
    
    try:
        # Get updates from bot
        url = f"https://api.telegram.org/bot{token}/getUpdates"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            if data['ok'] and data['result']:
                print("📱 Recent chats found:")
                print("-" * 30)
                
                for update in data['result']:
                    if 'message' in update:
                        message = update['message']
                        chat = message['chat']
                        
                        chat_id = chat['id']
                        chat_type = chat['type']
                        chat_title = chat.get('title', 'Private Chat')
                        username = chat.get('username', 'No Username')
                        
                        print(f"📋 Type: {chat_type}")
                        print(f"🆔 Chat ID: {chat_id}")
                        print(f"📛 Title: {chat_title}")
                        print(f"👤 Username: @{username}")
                        print("-" * 30)
            else:
                print("❌ No recent messages found.")
                print("💡 Send a message to your bot first!")
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    get_chat_id() 