# (c) ⚡𝗛𝗘𝗠𝗔𝗡𝗧𝗛⚡
# Username: @ALONEKINGSTAR77
# Main Link: https://t.me/otakustartelugu

import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

load_dotenv()

# Telegram API Configuration
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "8448505270:AAFg2Kd78sJHy8RvA5vmlc9xN6fvEJ0CuLA")
APP_ID = int(os.environ.get("APP_ID", "31355944"))
API_HASH = os.environ.get("API_HASH", "167e960d46363e3098f9c1fc78496adb")

# Database Configuration
DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://Hemanthmyname:9550399779htr@cluster0.o3qxb7m.mongodb.net/?appName=Cluster0")
DB_NAME = os.environ.get("DATABASE_NAME", "Cluster0")

# Owner / Admin Configuration
OWNER_ID = int(os.environ.get("OWNER_ID", "8557029592"))
OWNER = os.environ.get("OWNER", "ALONEKINGSTAR77")
ADMINS = [OWNER_ID]

# Force Subscribe Configuration
INITIAL_FSUB = [int(x.strip()) for x in os.environ.get("INITIAL_FSUB", "-1003376668245, -1003569023885").split(",") if x.strip()]
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1003444768506")) # Your db channel Id

# UI / Design Configuration
BOT_NAME = "⚡𝗛𝗘𝗠𝗔𝗡𝗧𝗛⚡"
BOT_USERNAME = "ALONEKINGSTAR77"
MAIN_LINK = "https://t.me/otakustartelugu"

PICS = [
    "https://freeimage.host/i/q94kIvp",
    "https://freeimage.host/i/q94kfZF",
    "https://freeimage.host/i/q94kn6J",
    "https://freeimage.host/i/q94kCGa",
    "https://freeimage.host/i/q94kTyN",
    "https://freeimage.host/i/q94kVuS",
    "https://freeimage.host/i/q94kRjt",
    "https://freeimage.host/i/q94kXt9",
    "https://freeimage.host/i/q94kwMu",
    "https://freeimage.host/i/q94kWw7",
    "https://freeimage.host/i/q94kN6b",
    "https://freeimage.host/i/q94kgwP",
    "https://freeimage.host/i/q94kv8Q",
    "https://freeimage.host/i/q94krt1",
    "https://freeimage.host/i/q94k6oF",
    "https://freeimage.host/i/q94kLKJ",
    "https://freeimage.host/i/q94kQcv",
    "https://freeimage.host/i/q94kD9p",
    "https://freeimage.host/i/q94kptt",
    "https://freeimage.host/i/q94kmNI"
]

LOG_CHANNEL = -1003562197365

# Random UI Images
START_PIC = os.environ.get("START_PIC", PICS[0])
FORCE_PIC = os.environ.get("FORCE_PIC", PICS[1])

# Bot Settings
URL = os.environ.get("URL", os.environ.get("RENDER_EXTERNAL_URL", os.environ.get("RAILWAY_STATIC_URL", "filestore-1-vlzn.onrender.com")))
PORT = os.environ.get("PORT", "8080")
FSUB_LINK_EXPIRY = int(os.getenv("FSUB_LINK_EXPIRY", "10"))
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "100"))
PROTECT_CONTENT = os.environ.get('PROTECT_CONTENT', "False").lower() == "true"
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", "False").lower() == "true"

# Shortlink Settings
SHORTLINK_URL = os.environ.get("SHORTLINK_URL", "mdiskshort.in/")
SHORTENER_PIC = os.environ.get("SHORTENER_PIC", "https://freeimage.host/i/q94kIvp")
SHORTLINK_API = os.environ.get("SHORTLINK_API", "7166158eb1d2cd04d15d274c891d47de7999e57a")
TUT_VID = os.environ.get("TUT_VID","https://t.me/otakustartelugu")
SHORT_MSG = "<b>⚡ Here is Your Download Link, Senpai! Must Watch Tutorial Before Clicking...</b>"

# Texts
USER_REPLY_TEXT = "<b>⚡ Please use the bot commands! 🏯</b>"
HELP_TXT = "<b>⚡ ʜᴇʟʟᴏ {mention}, I am {bot_name}!\n\nI can store files for you and provide links for them. 🏯\n\n<blockquote>◈ ᴄᴏᴍᴍᴀɴᴅs:\n├ /start - ᴄʜᴇᴄᴋ ɪғ ɪ ᴀᴍ ᴀʟɪᴠᴇ\n├ /about - ᴀʙᴏᴜᴛ ᴍᴇ\n└ /help - ᴛʜɪs ᴍᴇssᴀɢᴇ</blockquote>\n\nJoin our community: {main_link} ⭐</b>"
ABOUT_TXT = "<b><blockquote>⚡ ʙᴏᴛ ɴᴀᴍᴇ: {bot_name}\n🏯 ᴄʀᴇᴀᴛᴏʀ: {owner_name}\n⭐ ᴜsᴇʀɴᴀᴍᴇ: @{bot_username}\n🌸 ᴄᴏᴍᴍᴜɴɪᴛʏ: {main_link}\n💎 ᴅᴇᴠᴇʟᴏᴘᴇʀ: @ALONEKINGSTAR77</blockquote></b>"
START_MSG = "<b>⚡ Kon'nichiwa {mention}!\n\n<blockquote>I am {bot_name}, a powerful File Store Bot. 🏯\n\nI can store files in a private channel and users can access them via special links. Fast and Secure! ⭐</blockquote>\n\n🌸 Join @ALONEKINGSTAR77 for more updates!</b>"

FORCE_MSG = "<b>⚡ Kon'nichiwa {mention}!\n\n<blockquote>You must join our channels to access the requested file. 🏯</blockquote>\n\n🌸 Join the channels below and click on 'Reload' button. ⭐</b>"

# Premium Settings
PRICE1 = os.environ.get("PRICE1", "0 rs")
PRICE2 = os.environ.get("PRICE2", "60 rs")
PRICE3 = os.environ.get("PRICE3", "150 rs")
PRICE4 = os.environ.get("PRICE4", "280 rs")
PRICE5 = os.environ.get("PRICE5", "550 rs")
UPI_ID = os.environ.get("UPI_ID", "ALONEKINGSTAR77@upi")
SCREENSHOT_URL = os.environ.get("SCREENSHOT_URL", "https://t.me/ALONEKINGSTAR77")
QR_PIC = os.environ.get("QR_PIC", "https://freeimage.host/i/q94kIvp")

# Admin Texts
CMD_TXT = """<b>⚡ ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs:</b>

<b>›› /control_panel :</b> ʀᴇᴀʟ-ᴛɪᴍᴇ sᴇᴛᴛɪɴɢs
<b>›› /broadcast :</b> ʙʀᴏᴀᴅᴄᴀsᴛ ᴍᴇssᴀɢᴇ
<b>›› /stats :</b> ᴄʜᴇᴄᴋ ʙᴏᴛ sᴛᴀᴛs
<b>›› /batch :</b> ᴄʀᴇᴀᴛᴇ ʙᴀᴛᴄʜ ʟɪɴᴋ
<b>›› /genlink :</b> ɢᴇɴᴇʀᴀᴛᴇ sɪɴɢʟᴇ ʟɪɴᴋ
<b>›› /addfsub :</b> ᴀᴅᴅ ғsᴜʙ ᴄʜᴀɴɴᴇʟ
<b>›› /fsub_mode :</b> ᴛᴏɢɢʟᴇ ʀᴇǫᴜᴇsᴛ ᴍᴏᴅᴇ
<b>›› /maintenance :</b> ᴛᴏɢɢʟᴇ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ
<b>›› /ban :</b> ʙᴀɴ ᴀ ᴜsᴇʀ
<b>›› /unban :</b> ᴜɴʙᴀɴ ᴀ ᴜsᴇʀ
<b>›› /add_admin :</b> ᴀᴅᴅ ᴀᴅᴍɪɴ
<b>›› /addpremium :</b> ᴀᴅᴅ ᴘʀᴇᴍɪᴜᴍ
<b>›› /premium_users :</b> ʟɪsᴛ ᴘʀᴇᴍɪᴜᴍ
<b>›› /hash :</b> ᴍᴀsᴋɪɴɢ ᴍᴀɴᴀɢᴇ
<b>›› /count :</b> ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ᴄᴏᴜɴᴛs
"""

CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", "<b>⚡ ʙʏ {main_link}</b>")
if "{main_link}" in CUSTOM_CAPTION:
    CUSTOM_CAPTION = CUSTOM_CAPTION.format(main_link=MAIN_LINK)

BAN_SUPPORT = "https://t.me/otakustartelugu"
BOT_STATS_TEXT = "<b>⚡ BOT UPTIME</b>\n{uptime}"

# Logging Configuration
LOG_FILE_NAME = "bot.log"
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(LOG_FILE_NAME, maxBytes=50000000, backupCount=10),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
