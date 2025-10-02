import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DEFAULT_TZ = os.getenv("TZ", "Europe/Amsterdam")
