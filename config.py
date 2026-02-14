# (c) ⚡𝗛𝗘𝗠𝗔𝗡𝗧𝗛⚡
# Username: @ALONEKINGSTAR77
# Main Link: https://t.me/otakustartelugu

import os
import logging
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler

load_dotenv()

# Telegram API Configuration
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "8448505270:AAEwd0kQdkYmFbR9hMQQajTLwGj3M1gmIXQ")
APP_ID = int(os.environ.get("APP_ID", "31355944"))
API_HASH = os.environ.get("API_HASH", "167e960d46363e3098f9c1fc78496adb")

# Database Configuration
DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://botskingdom2:t7ognZuINrNfH3tj@cluster0.ystdy4m.mongodb.net/?retryWrites=true&w=majority")
DB_NAME = os.environ.get("DATABASE_NAME", "Cluster0")

# Owner / Admin Configuration
OWNER_ID = int(os.environ.get("OWNER_ID", "8557029592"))
OWNER = os.environ.get("OWNER", "ALONEKINGSTAR77")
ADMINS = [OWNER_ID]

# Force Subscribe Configuration
INITIAL_FSUB = [-1003884048084, -1003376668245, -1003569023885]
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1003444768506")) # Your db channel Id

# UI / Design Configuration
BOT_NAME = "⚡𝗛𝗘𝗠𝗔𝗡𝗧𝗛⚡"
MAIN_LINK = "https://t.me/otakustartelugu"

PICS = [
    "https://iili.io/q94kIvp.png",
    "https://iili.io/q94kfZF.png",
    "https://iili.io/q94kn6J.png",
    "https://iili.io/q94kCGa.png",
    "https://iili.io/q94kTyN.png",
    "https://iili.io/q94kVuS.png",
    "https://iili.io/q94kRjt.png",
    "https://iili.io/q94kXt9.png",
    "https://iili.io/q94kwMu.png",
    "https://iili.io/q94kWw7.png",
    "https://iili.io/q94kN6b.png",
    "https://iili.io/q94kgwP.png",
    "https://iili.io/q94kv8Q.png",
    "https://iili.io/q94krt1.png",
    "https://iili.io/q94k6oF.png",
    "https://iili.io/q94kLKJ.png",
    "https://iili.io/q94kQcv.png",
    "https://iili.io/q94kD9p.png",
    "https://iili.io/q94kptt.png",
    "https://iili.io/q94kmNI.png",
    "https://iili.io/qJHNJDb.png",
    "https://iili.io/qJHNHOu.png",
    "https://iili.io/qJHwyJ9.png",
    "https://iili.io/qJHN9Re.png",
    "https://iili.io/qJHN2xj.png",
    "https://iili.io/qJHNffV.png",
    "https://iili.io/qJHNFiQ.png",
    "https://iili.io/qJHNq0B.png",
    "https://iili.io/qJHeaNn.png",
    "https://iili.io/qJHNGzG.png",
    "https://iili.io/qJHO7Qj.png",
    "https://iili.io/qJHNpBR.png",
    "https://iili.io/qJHOiG4.png",
    "https://iili.io/qJHeHnj.png",
    "https://iili.io/qJHeMKl.png",
    "https://iili.io/qJHeVl2.png",
    "https://iili.io/qJHeWSS.png",
    "https://iili.io/qJHeeob.png",
    "https://iili.io/qJHewNe.png",
    "https://iili.io/qJHeUlV.png",
    "https://iili.io/qJHevix.png",
    "https://iili.io/qJHeSKQ.png",
    "https://iili.io/qJHeLxa.png",
    "https://iili.io/qJHe6R1.png",
    "https://iili.io/qJHkFsf.png",
    "https://iili.io/qJHkff4.png",
    "https://iili.io/qJHk9Rt.png",
    "https://iili.io/qJHkq0l.png",
    "https://iili.io/qJHkBg2.png",
    "https://iili.io/qJHko57.png",
    "https://iili.io/qJHkAsj.png",
    "https://iili.io/qJHkTzu.png"
]

# Random UI Images
START_PIC = PICS[0]
FORCE_PIC = PICS[1]

# Bot Settings
URL = os.environ.get("URL", "https://filestore-3-qhxv.onrender.com")
BOT_USERNAME = os.environ.get("BOT_USERNAME", "ALONEKINGSTAR77")
PORT = os.environ.get("PORT", "8080")
FSUB_LINK_EXPIRY = int(os.getenv("FSUB_LINK_EXPIRY", "10"))
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "500"))
PROTECT_CONTENT = os.environ.get('PROTECT_CONTENT', "False").lower() == "true"
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", "False").lower() == "true"

# Shortlink Settings
SHORTLINK_URL = os.environ.get("SHORTLINK_URL", "arolinks.com")
SHORTLINK_API = os.environ.get("SHORTLINK_API", "e49643875c2fa34dd6087254e58283d65ffc7748")
TUT_VID = os.environ.get("TUT_VID","https://t.me/otakustartelugu")
SHORT_MSG = "<b>⚡ Here is Your Download Link, Senpai! Must Watch Tutorial Before Clicking...</b>"

# Texts
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

<b>›› /broadcast :</b> ʙʀᴏᴀᴅᴄᴀsᴛ ᴍᴇssᴀɢᴇ
<b>›› /stats :</b> ᴄʜᴇᴄᴋ ʙᴏᴛ sᴛᴀᴛs
<b>›› /addfsub :</b> ᴀᴅᴅ ғsᴜʙ ᴄʜᴀɴɴᴇʟ
<b>›› /removefsub :</b> ʀᴇᴍᴏᴠᴇ ғsᴜʙ ᴄʜᴀɴɴᴇʟ
<b>›› /fsublist :</b> ʟɪsᴛ ғsᴜʙ ᴄʜᴀɴɴᴇʟs
<b>›› /ban :</b> ʙᴀɴ ᴀ ᴜsᴇʀ
<b>›› /unban :</b> ᴜɴʙᴀɴ ᴀ ᴜsᴇʀ
<b>›› /add_admin :</b> ᴀᴅᴅ ᴀᴅᴍɪɴ
<b>›› /deladmin :</b> ʀᴇᴍᴏᴠᴇ ᴀᴅᴍɪɴ
<b>›› /addpremium :</b> ᴀᴅᴅ ᴘʀᴇᴍɪᴜᴍ
<b>›› /myplan :</b> ᴄʜᴇᴄᴋ sᴛᴀᴛᴜs
"""

CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", "<b>⚡ ʙʏ {main_link}</b>")
if "{main_link}" in CUSTOM_CAPTION:
    CUSTOM_CAPTION = CUSTOM_CAPTION.format(main_link=MAIN_LINK)

BAN_SUPPORT = "https://t.me/otakustartelugu"
BOT_STATS_TEXT = "<b>⚡ BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "⚡ Kon'nichiwa! You are not my Senpai!"

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
