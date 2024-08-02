import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from pymongo import MongoClient
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import requests

response = requests.get('https://api.ipify.org?format=json')
ip = response.json()['ip']
print(f'Public IP Address: {ip}')


# Load the .env file
load_dotenv()

TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")
APP_ID = int(os.environ.get("APP_ID", "19277331"))
API_HASH = os.environ.get("API_HASH", "0df4b3b4eee9baa47694411eb4317115")


OWNER = os.environ.get("OWNER", "@ayan_alam")  # Owner username
OWNER_ID = int(os.environ.get("OWNER_ID", "1196934318"))  # Owner user id
DB_URL = os.environ.get("DB_URL", "")
DB_NAME = os.environ.get("DB_NAME", "")


CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1002169291947"))
FORCE_SUB_CHANNEL1 = int(os.environ.get(
    "FORCE_SUB_CHANNEL1", "0"))
FORCE_SUB_CHANNEL2 = int(os.environ.get(
    "FORCE_SUB_CHANNEL2", "0"))


SECONDS = int(os.getenv("SECONDS", "600"))  # auto delete in seconds


PORT = os.environ.get("PORT", "8080")
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "3"))


# start message
START_MSG = os.environ.get(
    "START_MESSAGE", "<b>🌸 𝙒𝙚𝙡𝙘𝙤𝙢𝙚, {first}!\n\n🌸 𝘿𝙞𝙫𝙚 𝙞𝙣𝙩𝙤 𝙩𝙝𝙚 𝙢𝙖𝙜𝙞𝙘 𝙤𝙛 𝙖𝙣𝙞𝙢𝙚 𝙬𝙝𝙚𝙧𝙚 𝙚𝙫𝙚𝙧𝙮 𝙨𝙩𝙤𝙧𝙮 𝙞𝙜𝙣𝙞𝙩𝙚𝙨 𝙮𝙤𝙪𝙧 𝙞𝙢𝙖𝙜𝙞𝙣𝙖𝙩𝙞𝙤𝙣. 𝙀𝙣𝙟𝙤𝙮 𝙮𝙤𝙪𝙧 𝙟𝙤𝙪𝙧𝙣𝙚𝙮 𝙬𝙞𝙩𝙝 𝙪𝙨! 🌟")

try:
    ADMINS = [1196934318]
    for x in (os.environ.get("ADMINS", "1196934318").split()):
        ADMINS.append(int(x))
except ValueError:
    raise Exception("Your Admins list does not contain valid integers.")


FORCE_MSG = os.environ.get(
    "FORCE_SUB_MESSAGE", "<b><center> 🌸 Hello, 𝙛𝙚𝙡𝙡𝙤𝙬 𝙤𝙩𝙖𝙠𝙪! 🌸 </center>\n\n 𝙃𝙚𝙧𝙚 𝙔𝙤𝙪 𝙃𝙖𝙫𝙚 𝙏𝙤 𝙅𝙤𝙞𝙣 𝙊𝙪𝙧 𝟐 𝘾𝙝𝙖𝙣𝙣𝙚𝙡𝙨, 𝙏𝙝𝙚𝙣 𝙔𝙤𝙪 𝘾𝙖𝙣 𝙐𝙨𝙚 𝙏𝙝𝙞𝙨 𝘽𝙤𝙩❗ 🎉 𝙇𝙚𝙩’𝙨 𝙨𝙥𝙧𝙞𝙣𝙠𝙡𝙚 𝙖 𝙡𝙞𝙩𝙩𝙡𝙚 “𝑱𝑨𝑷𝑨𝑵𝑬𝑺𝑬 𝐓𝐎𝐔𝐂𝐇” 𝙞𝙣𝙩𝙤 𝙤𝙪𝙧 𝙘𝙤𝙣𝙫𝙚𝙧𝙨𝙖𝙩𝙞𝙤𝙣𝙨, 𝙗𝙚𝙘𝙖𝙪𝙨𝙚 𝙡𝙞𝙛𝙚 𝙞𝙨 𝙗𝙚𝙩𝙩𝙚𝙧 𝙬𝙞𝙩𝒉 𝒊𝒕🌟</b>")

CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)

PROTECT_CONTENT = True if os.environ.get(
    'PROTECT_CONTENT', "False") == "True" else False

DISABLE_CHANNEL_BUTTON = os.environ.get(
    "DISABLE_CHANNEL_BUTTON", None) == 'True'

BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "❌ 𝙄 𝘼𝙈 𝘼 𝘽𝙊𝙏 𝙋𝙇𝙀𝘼𝙎𝙀 𝘿𝙊𝙉𝙏 𝙎𝙀𝙉𝘿 𝙈𝙀 𝙈𝙀𝙎𝙎𝘼𝙂𝙀𝙎!!"

ADMINS.append(OWNER_ID)
ADMINS.append(1768198143)

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


try:
    # Connect to MongoDB
    client = pymongo.MongoClient(DB_URL)
    db = client[DB_NAME]  # Specify the database to use
    print("Connected to MongoDB!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

client = MongoClient(DB_URL, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
