import os
from flask import Flask
import logging
from telegram import Bot

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Create the bot instance
TOKEN = os.getenv('TELEGRAM_TOKEN')  # Your Telegram bot token
bot = Bot(token=TOKEN)

@app.route('/')
def home():
    return "Telegram bot is running!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", "10000"))  # Use port from environment variable or default to 10000
    app.run(host='0.0.0.0', port=port)
