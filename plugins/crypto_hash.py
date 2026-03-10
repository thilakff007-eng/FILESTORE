# (c) ⚡𝗛𝗘𝗠𝗔𝗡𝗧𝗛⚡
# Link Masking & Hash Management

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from bot import Bot
from helper_func import admin, get_random_button_style
from database.database import db
import hashlib
import hmac
import os

# Available algorithms
ALGORITHMS = ["SHA-256", "SHA-512", "HMAC-SHA256", "BLAKE3", "AES-256", "ChaCha20", "Argon2", "scrypt"]

@Bot.on_message(filters.command("hash") & admin & filters.private)
async def hash_management_cmd(client: Client, message: Message):
    s, e = get_random_button_style()
    text = "<b>✧─── [ 🔐 ʟɪɴᴋ ᴍᴀsᴋɪɴɢ ᴍᴀɴᴀɢᴇ 🏯 ] ───✧</b>\n\n" \
           "Manage your link encryption and masking settings here. Choose an algorithm to toggle its status or set as primary. ⭐"

    current_algo = await db.get_setting("primary_hash_algo", "SHA-256")

    buttons = []
    # Create rows of 2 buttons
    for i in range(0, len(ALGORITHMS), 2):
        row = []
        for algo in ALGORITHMS[i:i+2]:
            prefix = "✅ " if algo == current_algo else ""
            row.append(InlineKeyboardButton(f"{prefix}{algo}", callback_data=f"set_hash_{algo}"))
        buttons.append(row)

    buttons.append([InlineKeyboardButton("• ᴄʟᴏsᴇ •", callback_data="close", icon_custom_emoji_id=e, style=s)])
    await message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))

@Bot.on_callback_query(filters.regex(r"^set_hash_"))
async def set_hash_callback(client: Client, query: CallbackQuery):
    algo = query.data.split("_")[-1]
    await db.set_setting("primary_hash_algo", algo)
    await query.answer(f"✅ Set {algo} as primary hashing algorithm!", show_alert=True)

    # Refresh the menu
    current_algo = algo
    buttons = []
    for i in range(0, len(ALGORITHMS), 2):
        row = []
        for a in ALGORITHMS[i:i+2]:
            prefix = "✅ " if a == current_algo else ""
            row.append(InlineKeyboardButton(f"{prefix}{a}", callback_data=f"set_hash_{a}"))
        buttons.append(row)

    s, e = get_random_button_style()
    buttons.append([InlineKeyboardButton("• ᴄʟᴏsᴇ •", callback_data="close", icon_custom_emoji_id=e, style=s)])

    await query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))
