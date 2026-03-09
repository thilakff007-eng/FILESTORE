# (c) ⚡𝗛𝗘𝗠𝗔𝗡𝗧𝗛⚡
# Link Masking & Hash Management

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from helper_func import admin, get_random_button_style
from database.database import db

@Bot.on_message(filters.command("hash") & admin & filters.private)
async def hash_management_cmd(client: Client, message: Message):
    s, e = get_random_button_style()
    text = "<b>✧─── [ 🔐 ʟɪɴᴋ ᴍᴀsᴋɪɴɢ ᴍᴀɴᴀɢᴇ 🏯 ] ───✧</b>\n\n" \
           "Manage your link encryption and masking settings here. Choose an algorithm to toggle its status. ⭐"

    # Simple mockup for now as the actual crypto logic is in a different module if it exists
    buttons = [
        [InlineKeyboardButton("AES-256", callback_data="toggle_hash_aes"), InlineKeyboardButton("SHA-256", callback_data="toggle_hash_sha")],
        [InlineKeyboardButton("ChaCha20", callback_data="toggle_hash_chacha"), InlineKeyboardButton("Argon2", callback_data="toggle_hash_argon")],
        [InlineKeyboardButton("• ᴄʟᴏsᴇ •", callback_data="close", icon_custom_emoji_id=e, style=s)]
    ]
    await message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))
