import os
import logging
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
TRANSCRIBE_API = os.getenv("TRANSCRIBE_API")

if not BOT_TOKEN:
    logging.error("BOT_TOKEN environment variable not set. Please set it or create a .env file with BOT_TOKEN=YOUR_BOT_TOKEN.")
    exit(1)
