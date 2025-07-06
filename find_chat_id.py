import telebot
import requests

# Your bot token
token = "7893259724:AAFfxQ5TuhiHtv9hr6QGBg524d0p-vaFGaI"
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['chatid'])
def get_chat_id(message):
    chat_id = message.chat.id
    chat_type = message.chat.type
    chat_title = message.chat.title or "Private Chat"
    
    response = f"""
🔍 <b>Chat Information</b>

📋 <b>Chat Type:</b> {chat_type}
🆔 <b>Chat ID:</b> <code>{chat_id}</code>
📛 <b>Chat Title:</b> {chat_title}

💡 <b>How to use:</b>
• For private chats: Use the ID as is
• For groups: Add minus sign (-) before the ID
• For channels: Add -100 before the ID
"""
    
    bot.reply_to(message, response, parse_mode="HTML")

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    bot.reply_to(message, f"👋 Hi! Send /chatid to get this chat's ID.\n\nYour current chat ID is: <code>{chat_id}</code>", parse_mode="HTML")

print("Chat ID Finder Bot Started!")
print("Send /chatid to any chat to get its ID")
bot.infinity_polling() 