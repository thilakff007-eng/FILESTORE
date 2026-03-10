
# (©) @ALONEKINGSTAR77
# Premium Management Plugin

from pyrogram import Client, filters
from pyrogram.enums import ButtonStyle
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from bot import Bot
from config import OWNER_ID
from database.db_premium import add_premium, remove_premium, get_all_premium_users, get_premium_count
from helper_func import admin, get_random_button_style
import pyromod

@Bot.on_message(filters.command("addpremium") & admin & filters.private)
async def add_premium_cmd(client, message):
    try:
        # Step 1: User ID
        ask_id = await message.chat.ask("<b>Please Enter the User ID of the User you want to add Premium for:</b>", filters=filters.text, timeout=60)
        try:
            user_id = int(ask_id.text)
        except ValueError:
            return await message.reply("<b>❌ Invalid User ID. Please try again with a numeric ID. /addpremium</b>")

        # Step 2: Days
        ask_days = await message.chat.ask("<b>Please Enter the number of days you want to add Premium for:</b>", filters=filters.text, timeout=60)
        try:
            days = int(ask_days.text)
        except ValueError:
            return await message.reply("<b>❌ Invalid number of days. Please try again with a numeric value. /addpremium</b>")

        # Step 3: Add and Confirm
        expiry = await add_premium(user_id, days, 'd')
        await message.reply(f"<b>✅ Premium Added Successfully!</b>\n\n<b>User ID:</b> <code>{user_id}</code>\n<b>Duration:</b> <code>{days} Days</code>\n<b>Expiry:</b> <code>{expiry}</code>")
    except Exception as e:
        await message.reply(f"<b>❌ Error:</b> <code>{e}</code>")

@Bot.on_message(filters.command(["premium_users", "listpremium"]) & admin & filters.private)
async def list_premium_cmd(client, message):
    users = await get_all_premium_users()
    count = len(users)

    text = f"<b>⚡ PREMIUM USERS LIST ⚡</b>\n\n"
    text += f"<b>Total Premium Users:</b> <code>{count}</code>\n\n"

    if count == 0:
        text += "<i>No premium users found.</i>"
        s, e = get_random_button_style()
        buttons = [[InlineKeyboardButton("❌ Close", callback_data="close", icon_custom_emoji_id=e, style=s)]]
    else:
        text += "<b>Select a user to manage:</b>"
        buttons = []
        for user in users:
            u_id = user['user_id']
            # Try to get user info for name
            try:
                u_info = await client.get_users(u_id)
                name = u_info.first_name
            except:
                name = "Unknown"

            rem_days = int(user['remaining_seconds'] // (24 * 3600))
            s, e = get_random_button_style()
            buttons.append([InlineKeyboardButton(f"👤 {name} ({u_id}) - {rem_days}d", callback_data=f"manage_prem_{u_id}", icon_custom_emoji_id=e, style=s)])

        s, e = get_random_button_style()
        buttons.append([InlineKeyboardButton("❌ Close", callback_data="close", icon_custom_emoji_id=e, style=s)])

    await message.reply(text, reply_markup=InlineKeyboardMarkup(buttons))

# Callback handlers moved to cbb.py to resolve dispatcher lag and conflicts

@Bot.on_message(filters.command("remove_premium") & admin & filters.private)
async def remove_premium_cmd(client, message):
    if len(message.command) < 2:
        return await message.reply("<b>Usage: /remove_premium {user_id}</b>")
    try:
        user_id = int(message.command[1])
        await remove_premium(user_id)
        await message.reply(f"<b>✅ Premium Access Revoked for <code>{user_id}</code>.</b>")
    except ValueError:
        await message.reply("<b>❌ Invalid User ID.</b>")
    except Exception as e:
        await message.reply(f"<b>❌ Error:</b> <code>{e}</code>")
