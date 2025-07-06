#!/bin/bash

echo "🚀 Setting up Telegram Bot as System Service..."

# Copy service file to systemd directory
cp telegram-bot.service /etc/systemd/system/

# Reload systemd
systemctl daemon-reload

# Enable service to start on boot
systemctl enable telegram-bot

# Start the service
systemctl start telegram-bot

# Check status
systemctl status telegram-bot

echo "✅ Service setup complete!"
echo ""
echo "📋 Management Commands:"
echo "  Start:   sudo systemctl start telegram-bot"
echo "  Stop:    sudo systemctl stop telegram-bot"
echo "  Restart: sudo systemctl restart telegram-bot"
echo "  Status:  sudo systemctl status telegram-bot"
echo "  Logs:    sudo journalctl -u telegram-bot -f"
echo ""
echo "🔄 The bot will now:"
echo "  • Start automatically on boot"
echo "  • Restart automatically if it crashes"
echo "  • Run continuously in the background" 