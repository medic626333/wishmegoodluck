# Telegram Bot VPS Deployment Guide

## 🚀 Quick Setup

### Step 1: Run the Setup Script
```bash
# Download and run the setup script
wget https://raw.githubusercontent.com/your-repo/vps_setup.sh
chmod +x vps_setup.sh
./vps_setup.sh
```

### Step 2: Upload Bot Files
Upload these files to your VPS in the `~/telegram_bot/` directory:
- `main.py` (your bot code)
- `gatet.py` (gate checking module)

### Step 3: Create Required Files
```bash
cd ~/telegram_bot

# Create id.txt with authorized users
echo "7736734364" > id.txt
# Add more user IDs as needed

# Create empty files
touch combo.txt
```

### Step 4: Start the Bot
```bash
# Start the bot service
sudo systemctl start telegram-bot

# Check status
sudo systemctl status telegram-bot

# View logs
sudo journalctl -u telegram-bot -f
```

## 🔧 Management Commands

### Start Bot
```bash
./start_bot.sh
# or
sudo systemctl start telegram-bot
```

### Stop Bot
```bash
./stop_bot.sh
# or
sudo systemctl stop telegram-bot
```

### Restart Bot
```bash
./restart_bot.sh
# or
sudo systemctl restart telegram-bot
```

### Check Status
```bash
./status_bot.sh
# or
sudo systemctl status telegram-bot
```

### View Logs
```bash
./logs_bot.sh
# or
sudo journalctl -u telegram-bot -f
```

## 📁 File Structure
```
~/telegram_bot/
├── main.py              # Main bot code
├── gatet.py             # Gate checking module
├── id.txt               # Authorized user IDs
├── combo.txt            # Temporary file for card processing
├── requirements.txt     # Python dependencies
├── venv/                # Python virtual environment
├── start_bot.sh         # Start script
├── stop_bot.sh          # Stop script
├── restart_bot.sh       # Restart script
├── status_bot.sh        # Status script
└── logs_bot.sh          # Logs script
```

## 🔍 Troubleshooting

### Bot Not Starting
```bash
# Check logs
sudo journalctl -u telegram-bot -n 50

# Check file permissions
ls -la ~/telegram_bot/

# Check Python environment
cd ~/telegram_bot
source venv/bin/activate
python -c "import telebot; print('Telegram bot library OK')"
```

### Permission Issues
```bash
# Fix ownership
sudo chown -R $USER:$USER ~/telegram_bot/

# Fix permissions
chmod +x ~/telegram_bot/*.sh
```

### Update Bot Code
```bash
# Stop bot
sudo systemctl stop telegram-bot

# Upload new files
# (Upload your updated main.py and gatet.py)

# Start bot
sudo systemctl start telegram-bot
```

## 📊 Monitoring

### Check Bot Status
```bash
sudo systemctl status telegram-bot
```

### View Real-time Logs
```bash
sudo journalctl -u telegram-bot -f
```

### Check Resource Usage
```bash
# Check CPU and memory usage
ps aux | grep python

# Check disk usage
df -h
```

## 🔒 Security Tips

1. **Keep your bot token secure**
2. **Regularly update system packages**
3. **Use firewall rules if needed**
4. **Monitor logs for suspicious activity**
5. **Backup your bot files regularly**

## 🆘 Emergency Commands

### Force Stop All Python Processes
```bash
pkill -f python
```

### Reset Bot Service
```bash
sudo systemctl reset-failed telegram-bot
sudo systemctl start telegram-bot
```

### Complete Reinstall
```bash
sudo systemctl stop telegram-bot
sudo systemctl disable telegram-bot
sudo rm /etc/systemd/system/telegram-bot.service
sudo systemctl daemon-reload
# Then run setup script again
```

---

**Need Help?** Check the logs first: `sudo journalctl -u telegram-bot -n 100` 