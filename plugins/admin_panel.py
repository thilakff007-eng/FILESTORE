# (c) ⚡𝗛𝗘𝗠𝗔𝗡𝗧𝗛⚡

import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, LinkPreviewOptions
from bot import Bot
from config import OWNER_ID
from helper_func import get_random_button_style, admin
from database.database import db

async def get_control_panel_markup(client):
    s1, e1 = get_random_button_style()
    s2, e2 = get_random_button_style()
    s3, e3 = get_random_button_style()
    s4, e4 = get_random_button_style()
    s5, e5 = get_random_button_style()
    s6, e6 = get_random_button_style()

    shortener_enabled = await db.get_shortener_status()
    del_timer = await db.get_del_timer()
    is_tutorial = await db.get_setting("is_tutorial", True)
    protect_content = await db.get_protect_content()

    shortener_text = "🟢 ᴏɴ" if shortener_enabled else "🔴 ᴏғғ"
    tut_text = "🟢 ᴏɴ" if is_tutorial else "🔴 ᴏғғ"
    protect_text = "🟢 ᴏɴ" if protect_content else "🔴 ᴏғғ"

    buttons = [
        [
            InlineKeyboardButton(f"🔗 sʜᴏʀᴛᴇɴᴇʀ: {shortener_text}", callback_data="cp_toggle_shortener", style=s1, icon_custom_emoji_id=e1),
            InlineKeyboardButton(f"🎥 ᴛᴜᴛᴏʀɪᴀʟ: {tut_text}", callback_data="cp_toggle_tutorial", style=s2, icon_custom_emoji_id=e2)
        ],
        [
            InlineKeyboardButton(f"🚫 ᴘʀᴏᴛᴇᴄᴛ: {protect_text}", callback_data="cp_toggle_protect", style=s3, icon_custom_emoji_id=e3),
            InlineKeyboardButton(f"🗑️ ᴀᴜᴛᴏ ᴅᴇʟ: {del_timer}s", callback_data="cp_set_del_timer", style=s4, icon_custom_emoji_id=e4)
        ],
        [
            InlineKeyboardButton("📊 sᴛᴀᴛs", callback_data="stats", style=s5, icon_custom_emoji_id=e5),
            InlineKeyboardButton("📢 ᴍᴀɴᴀɢᴇ ғsᴜʙ", callback_data="cp_manage_fsub", style=s6, icon_custom_emoji_id=e6)
        ],
        [
            InlineKeyboardButton("❌ ᴄʟᴏsᴇ ❌", callback_data="close", style=s1, icon_custom_emoji_id=e1)
        ]
    ]
    return InlineKeyboardMarkup(buttons)

@Bot.on_message(filters.private & filters.command("control_panel") & admin)
async def control_panel_cmd(client: Client, message: Message):
    await message.reply_text(
        "<b>✧─── [ ⚡ ᴀᴅᴍɪɴ ᴄᴏɴᴛʀᴏʟ ᴘᴀɴᴇʟ 🏯 ] ───✧</b>\n\n"
        "Welcome Senpai! Here you can manage all the bot's core variables and settings in real-time. ⭐",
        reply_markup=await get_control_panel_markup(client)
    )

# Callback handlers moved to cbb.py to resolve dispatcher lag and conflicts

async def get_fsub_management_markup():
    s1, e1 = get_random_button_style()
    s2, e2 = get_random_button_style()
    s3, e3 = get_random_button_style()
    s4, e4 = get_random_button_style()

    buttons = [
        [
            InlineKeyboardButton("➕ ᴀᴅᴅ ᴄʜᴀɴɴᴇʟ", callback_data="cp_add_fsub", style=s1, icon_custom_emoji_id=e1),
            InlineKeyboardButton("➖ ʀᴇᴍᴏᴠᴇ ᴄʜᴀɴɴᴇʟ", callback_data="cp_rem_fsub", style=s2, icon_custom_emoji_id=e2)
        ],
        [
            InlineKeyboardButton("📋 ʟɪsᴛ & ᴛᴏɢɢʟᴇ ᴍᴏᴅᴇ", callback_data="fsub_back", style=s3, icon_custom_emoji_id=e3)
        ],
        [
            InlineKeyboardButton("‹ ʙᴀᴄᴋ", callback_data="cp_back", style=s4, icon_custom_emoji_id=e4)
        ]
    ]
    return InlineKeyboardMarkup(buttons)

# Callback handlers moved to cbb.py to resolve dispatcher lag and conflicts
