#!/bin/bash

echo "🚀 Setting up Auto-Restart for Telegram Bot..."

# Get current directory
CURRENT_DIR=$(pwd)
BOT_USER=$(whoami)

echo "📁 Bot directory: $CURRENT_DIR"
echo "👤 Bot user: $BOT_USER"

# Create systemd service file
echo "📝 Creating systemd service file..."
sudo tee /etc/systemd/system/telegram-bot.service > /dev/null <<EOF
[Unit]
Description=Telegram Card Checker Bot
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
User=$BOT_USER
WorkingDirectory=$CURRENT_DIR
ExecStart=$CURRENT_DIR/venv/bin/python $CURRENT_DIR/main.py
Restart=always
RestartSec=10
StartLimitBurst=5
StartLimitIntervalSec=60

# Environment variables
Environment=PATH=$CURRENT_DIR/venv/bin
Environment=PYTHONPATH=$CURRENT_DIR

# Logging
StandardOutput=journal
StandardError=journal
SyslogIdentifier=telegram-bot

# Security settings
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF

# Set proper permissions
echo "🔒 Setting permissions..."
chmod +x main.py
chmod +x bot_runner.py
chmod 600 id.txt

# Reload systemd and enable service
echo "⚙️ Configuring systemd service..."
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot.service

# Create log directory
sudo mkdir -p /var/log/telegram-bot
sudo chown $BOT_USER:$BOT_USER /var/log/telegram-bot

# Create monitoring script
echo "📊 Creating monitoring script..."
cat > monitor_bot.sh << 'MONITOR_EOF'
#!/bin/bash

echo "🔍 Telegram Bot Status Monitor"
echo "================================"

# Check service status
echo "📊 Service Status:"
sudo systemctl status telegram-bot.service --no-pager -l

echo ""
echo "📋 Recent Logs (last 20 lines):"
sudo journalctl -u telegram-bot.service -n 20 --no-pager

echo ""
echo "🔄 Service Management Commands:"
echo "  Start:   sudo systemctl start telegram-bot.service"
echo "  Stop:    sudo systemctl stop telegram-bot.service"
echo "  Restart: sudo systemctl restart telegram-bot.service"
echo "  Logs:    sudo journalctl -u telegram-bot.service -f"
MONITOR_EOF

chmod +x monitor_bot.sh

# Create management script
echo "🛠️ Creating management script..."
cat > manage_bot.sh << 'MANAGE_EOF'
#!/bin/bash

case "$1" in
    start)
        echo "🚀 Starting Telegram Bot..."
        sudo systemctl start telegram-bot.service
        ;;
    stop)
        echo "🛑 Stopping Telegram Bot..."
        sudo systemctl stop telegram-bot.service
        ;;
    restart)
        echo "🔄 Restarting Telegram Bot..."
        sudo systemctl restart telegram-bot.service
        ;;
    status)
        echo "📊 Bot Status:"
        sudo systemctl status telegram-bot.service
        ;;
    logs)
        echo "📋 Bot Logs (Press Ctrl+C to exit):"
        sudo journalctl -u telegram-bot.service -f
        ;;
    enable)
        echo "✅ Enabling auto-start on boot..."
        sudo systemctl enable telegram-bot.service
        ;;
    disable)
        echo "❌ Disabling auto-start on boot..."
        sudo systemctl disable telegram-bot.service
        ;;
    *)
        echo "🤖 Telegram Bot Management Script"
        echo "Usage: $0 {start|stop|restart|status|logs|enable|disable}"
        echo ""
        echo "Commands:"
        echo "  start    - Start the bot"
        echo "  stop     - Stop the bot"
        echo "  restart  - Restart the bot"
        echo "  status   - Show bot status"
        echo "  logs     - Show live logs"
        echo "  enable   - Enable auto-start on boot"
        echo "  disable  - Disable auto-start on boot"
        ;;
esac
MANAGE_EOF

chmod +x manage_bot.sh

echo ""
echo "✅ Auto-restart setup completed!"
echo ""
echo "🎯 Quick Start Commands:"
echo "  Start bot:     ./manage_bot.sh start"
echo "  Check status:  ./manage_bot.sh status"
echo "  View logs:     ./manage_bot.sh logs"
echo "  Monitor bot:   ./monitor_bot.sh"
echo ""
echo "🔄 The bot will now automatically restart if it crashes!"
echo "🚀 The bot will start automatically when the VPS boots!"
echo ""
echo "📋 To start the bot now, run:"
echo "   sudo systemctl start telegram-bot.service"
