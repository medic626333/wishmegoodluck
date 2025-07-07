# Credit Card Checker Bot

A Telegram bot for checking credit card validity with advanced features including cooldown timers, batch processing, and owner notifications.

## Features

### Core Functionality
- **Single Card Check** (`/chk`): Check individual credit cards with 20-second cooldown for users
- **Bulk Card Check**: Process multiple cards from uploaded files (up to 2000 cards)
- **Real-time BIN Information**: Fetches bank, country, and card type details
- **Gateway Integration**: Uses Stripe-based payment gateway for validation

### User Management
- **Authorization System**: User whitelist with `/add` and `/remove` commands
- **Owner Privileges**: Special permissions for bot owners
- **Redeem Codes**: Generate and redeem access codes
- **User Information**: View user details and authorization status

### Advanced Features
- **Cooldown Timer**: 20-second cooldown for `/chk` command (users only, owners exempt)
- **Silent Owner Notifications**: Owners receive notifications without user awareness
- **Batch Processing**: Check multiple cards with detailed responses
- **Rate Limiting**: Automatic breaks during bulk processing to prevent gateway overload
- **Stop Functionality**: Ability to halt bulk checking operations

## Commands

### User Commands
- `/start` - Initialize bot and check authorization
- `/help` - Display available commands
- `/chk <card>` - Check single card (format: `4111111111111111|12|25|123`)
- `/info` - View your user information and status
- `/redeem <code>` - Redeem access code

### Owner Commands
- `/add <user_id>` - Add user to authorized list
- `/remove <user_id>` - Remove user from authorized list
- `/code` - Generate new redeem code
- `/show_auth_users` - View all authorized users

## Installation

1. Clone the repository:
```bash
git clone https://github.com/medic626333/wishmegoodluck.git
cd wishmegoodluck
```

2. Install dependencies:
```bash
pip install requests telebot
```

3. Configure the bot:
   - Update the bot token in `main.py`
   - Set owner ID in the `owners` list
   - Create `id.txt` file for authorized users

4. Run the bot:
```bash
python main.py
```

## Configuration

### Bot Settings
- **Token**: Update `token` variable in `main.py`
- **Owner ID**: Modify `owners` list with your Telegram user ID
- **Allowed Group**: Set `allowed_group` for `/chk` command usage
- **Logs Group**: Configure `LOGS_GROUP_CHAT_ID` for logging

### Files
- `id.txt` - Contains authorized user IDs (one per line)
- `combo.txt` - Temporary file for bulk card processing
- `gatet.py` - Gateway integration module

## Security Features

- **User Authorization**: Only whitelisted users can access the bot
- **Group Restrictions**: `/chk` command limited to specific group
- **Owner Verification**: Administrative commands require owner privileges
- **Silent Notifications**: Owner alerts without user notification
- **Rate Limiting**: Prevents gateway abuse

## Cooldown System

The bot implements a smart cooldown system:
- **Regular Users**: 20-second cooldown between `/chk` commands
- **Owners**: No cooldown restrictions
- **Precise Timing**: Shows exact remaining time to users
- **Memory Efficient**: Only tracks active users

## Gateway Integration

- **Stripe Integration**: Uses Stripe payment processing for card validation
- **BIN Lookup**: Fetches detailed card information from BIN database
- **Response Parsing**: Intelligent parsing of gateway responses
- **Error Handling**: Comprehensive error detection and reporting

## File Structure

```
├── main.py              # Main bot application
├── gatet.py             # Gateway integration
├── bot_manager.py       # Bot management utilities
├── id.txt               # Authorized user IDs
├── combo.txt            # Temporary card data
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational purposes only. Use responsibly and in accordance with applicable laws and regulations.

## Support

For support or questions, contact the repository owner.

---

**Note**: This bot is designed for legitimate card validation purposes only. Ensure compliance with all applicable laws and payment processor terms of service.
