#!/bin/bash

echo "🚀 Starting VPS Setup for Telegram Bot..."

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python and pip
echo "🐍 Installing Python and pip..."
sudo apt install python3 python3-pip python3-venv -y

# Install git
echo "📥 Installing git..."
sudo apt install git -y

# Create bot directory
echo "📁 Creating bot directory..."
mkdir -p ~/telegram_bot
cd ~/telegram_bot

# Create virtual environment
echo "🔧 Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install required packages
echo "📚 Installing required packages..."
pip install --upgrade pip
pip install pyTelegramBotAPI requests

# Create requirements.txt
echo "📝 Creating requirements.txt..."
cat > requirements.txt << EOF
pyTelegramBotAPI==4.14.0
requests==2.31.0
urllib3==2.0.7
EOF

# Create systemd service file
echo "⚙️ Creating systemd service..."
sudo tee /etc/systemd/system/telegram-bot.service > /dev/null << EOF
[Unit]
Description=Telegram Card Checker Bot
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/home/$USER/telegram_bot
Environment=PATH=/home/$USER/telegram_bot/venv/bin
ExecStart=/home/$USER/telegram_bot/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Create startup script
echo "🔄 Creating startup script..."
cat > start_bot.sh << 'EOF'
#!/bin/bash
cd ~/telegram_bot
source venv/bin/activate
python main.py
EOF

chmod +x start_bot.sh

# Create stop script
echo "🛑 Creating stop script..."
cat > stop_bot.sh << 'EOF'
#!/bin/bash
sudo systemctl stop telegram-bot
echo "Bot stopped successfully!"
EOF

chmod +x stop_bot.sh

# Create restart script
echo "🔄 Creating restart script..."
cat > restart_bot.sh << 'EOF'
#!/bin/bash
sudo systemctl restart telegram-bot
echo "Bot restarted successfully!"
EOF

chmod +x restart_bot.sh

# Create status script
echo "📊 Creating status script..."
cat > status_bot.sh << 'EOF'
#!/bin/bash
sudo systemctl status telegram-bot
EOF

chmod +x status_bot.sh

# Create logs script
echo "📋 Creating logs script..."
cat > logs_bot.sh << 'EOF'
#!/bin/bash
sudo journalctl -u telegram-bot -f
EOF

chmod +x logs_bot.sh

# Reload systemd
echo "🔄 Reloading systemd..."
sudo systemctl daemon-reload

# Enable service
echo "✅ Enabling bot service..."
sudo systemctl enable telegram-bot

echo ""
echo "🎉 VPS Setup Complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Upload your main.py and gatet.py files to ~/telegram_bot/"
echo "2. Create id.txt file with authorized user IDs"
echo "3. Start the bot: ./start_bot.sh"
echo ""
echo "🔧 Available Commands:"
echo "  ./start_bot.sh   - Start the bot"
echo "  ./stop_bot.sh    - Stop the bot"
echo "  ./restart_bot.sh - Restart the bot"
echo "  ./status_bot.sh  - Check bot status"
echo "  ./logs_bot.sh    - View bot logs"
echo ""
echo "📁 Bot Directory: ~/telegram_bot/"
echo "📝 Logs: sudo journalctl -u telegram-bot -f"
echo ""
echo "🚀 Your bot is ready for deployment!" 