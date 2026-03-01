# (c) ⚡𝗛𝗘𝗠𝗔𝗡𝗧𝗛⚡

import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
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

    shortener_enabled = await db.get_shortener_status()
    del_timer = await db.get_del_timer()

    # We can also add other settings from DB if we implement them
    # For now let's stick to the requested ones and maybe a few more

    shortener_text = "🟢 ᴏɴ" if shortener_enabled else "🔴 ᴏғғ"

    # Check extra settings
    is_tutorial = await db.get_setting("is_tutorial", True)
    tut_text = "🟢 ᴏɴ" if is_tutorial else "🔴 ᴏғғ"

    buttons = [
        [
            InlineKeyboardButton(f"🔗 sʜᴏʀᴛᴇɴᴇʀ: {shortener_text}", callback_data="cp_toggle_shortener", style=s1, icon_custom_emoji_id=e1),
            InlineKeyboardButton(f"🎥 ᴛᴜᴛᴏʀɪᴀʟ: {tut_text}", callback_data="cp_toggle_tutorial", style=s2, icon_custom_emoji_id=e2)
        ],
        [
            InlineKeyboardButton(f"🗑️ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ: {del_timer}s", callback_data="cp_set_del_timer", style=s3, icon_custom_emoji_id=e3)
        ],
        [
            InlineKeyboardButton("📊 sᴛᴀᴛs", callback_data="stats", style=s4, icon_custom_emoji_id=e4),
            InlineKeyboardButton("📢 ғsᴜʙ ʟɪsᴛ", callback_data="fsub_back", style=s5, icon_custom_emoji_id=e5)
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

@Bot.on_callback_query(filters.regex("^cp_toggle_shortener$"))
async def toggle_shortener_cb(client: Client, callback_query: CallbackQuery):
    if callback_query.from_user.id != OWNER_ID and not await db.admin_exist(callback_query.from_user.id):
        return await callback_query.answer("⚠️ Access Denied! You are not my Senpai!", show_alert=True)

    current_status = await db.get_shortener_status()
    new_status = not current_status
    await db.set_shortener_status(new_status)

    await callback_query.message.edit_reply_markup(
        reply_markup=await get_control_panel_markup(client)
    )
    await callback_query.answer(f"✅ Shortener {'Enabled' if new_status else 'Disabled'}!")

@Bot.on_callback_query(filters.regex("^cp_toggle_tutorial$"))
async def toggle_tutorial_cb(client: Client, callback_query: CallbackQuery):
    if callback_query.from_user.id != OWNER_ID and not await db.admin_exist(callback_query.from_user.id):
        return await callback_query.answer("⚠️ Access Denied!", show_alert=True)

    current_status = await db.get_setting("is_tutorial", True)
    new_status = not current_status
    await db.set_setting("is_tutorial", new_status)

    await callback_query.message.edit_reply_markup(
        reply_markup=await get_control_panel_markup(client)
    )
    await callback_query.answer(f"✅ Tutorial {'Enabled' if new_status else 'Disabled'}!")

@Bot.on_callback_query(filters.regex("^cp_set_del_timer$"))
async def set_del_timer_cb(client: Client, callback_query: CallbackQuery):
    if callback_query.from_user.id != OWNER_ID and not await db.admin_exist(callback_query.from_user.id):
        return await callback_query.answer("Access Denied!", show_alert=True)

    await callback_query.answer()

    # Using client.ask for interactive update
    try:
        timer_msg = await client.ask(
            chat_id=callback_query.from_user.id,
            text="<b>Please send the new Auto Delete Timer in seconds.</b>\n\n<i>Example: 600 for 10 minutes.</i>",
            timeout=60
        )
    except:
        return

    try:
        new_timer = int(timer_msg.text)
        await db.set_del_timer(new_timer)
        await timer_msg.reply_text(f"✅ Auto Delete Timer updated to {new_timer} seconds.")

        # Refresh control panel
        await callback_query.message.edit_reply_markup(
        reply_markup=await get_control_panel_markup(client)
        )
    except ValueError:
        await timer_msg.reply_text("❌ Invalid input! Please send a number.")
