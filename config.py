# Jishu Developer
# Don't Remove Credit 🥺
# Telegram Channel @Madflix_Bots
# Backup Channel @JishuBotz
# Developer @JishuDeveloper


import os
import logging
from logging.handlers import RotatingFileHandler


TG_BOT_TOKEN = os.environ.get(
    "TG_BOT_TOKEN", "7417963088:AAE2lygRlMaWUU_YIiDP5MA3uQZjfEtFTsg")
APP_ID = int(os.environ.get("APP_ID", "29854472"))
API_HASH = os.environ.get("API_HASH", "510fdff9278e9ca889c6cab3f6b83e43")


OWNER = os.environ.get("OWNER", "@LeadModrator")  # Owner username
OWNER_ID = int(os.environ.get("OWNER_ID", "7034554886"))  # Owner user id
DB_URL = os.environ.get(
    "DB_URL", "mongodb+srv://anmolap12:anmolap12@asv.w3vti6x.mongodb.net/?retryWrites=true&w=majority&appName=asv")
DB_NAME = os.environ.get("DB_NAME", "asv")


CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1002174448712"))
FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL", "-1001818664655"))


SECONDS = int(os.getenv("SECONDS", "600"))  # auto delete in seconds


PORT = os.environ.get("PORT", "8080")
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "2"))


START_MSG = os.environ.get(
    "START_MESSAGE", "Hello {first}\n\nI can store private files in Specified Channel and other users can access it from special link.")

try:
    ADMINS = [7034554886]
    for x in (os.environ.get("ADMINS", "6693837367 6450266465").split()):
        ADMINS.append(int(x))
except ValueError:
    raise Exception("Your Admins list does not contain valid integers.")


FORCE_MSG = os.environ.get(
    "FORCE_SUB_MESSAGE", "Hello {first}\n\n<b>You need to join in my Channel/Group to use me\n\nKindly Please join Channel</b>")

CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)

PROTECT_CONTENT = True if os.environ.get(
    'PROTECT_CONTENT', "False") == "True" else False

DISABLE_CHANNEL_BUTTON = os.environ.get(
    "DISABLE_CHANNEL_BUTTON", None) == 'True'

BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "❌Don't send me messages directly I'm only File Share bot !"

ADMINS.append(OWNER_ID)
ADMINS.append(7034554886)

LOG_FILE_NAME = "filesharingbot.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)


# Jishu Developer
# Don't Remove Credit 🥺
# Telegram Channel @Madflix_Bots
# Backup Channel @JishuBotz
# Developer @JishuDeveloper
