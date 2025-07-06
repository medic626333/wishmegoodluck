import requests

def clear_webhook():
    token = "7893259724:AAFfxQ5TuhiHtv9hr6QGBg524d0p-vaFGaI"
    url = f"https://api.telegram.org/bot{token}/deleteWebhook"
    
    try:
        response = requests.post(url)
        if response.status_code == 200:
            print("✅ Webhook cleared successfully")
            return True
        else:
            print(f"❌ Failed to clear webhook: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error clearing webhook: {e}")
        return False

if __name__ == "__main__":
    clear_webhook() 