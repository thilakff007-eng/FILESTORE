
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

@Bot.on_message(filters.command("listpremium") & admin & filters.private)
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

@Bot.on_callback_query(filters.regex(r"^manage_prem_(\d+)"))
async def manage_premium_callback(client, query: CallbackQuery):
    user_id = int(query.data.split("_")[-1])

    # Show sub-menu
    text = f"<b>💎 Managing User:</b> <code>{user_id}</code>\n\nChoose an action:"
    s1, e1 = get_random_button_style()
    s2, e2 = get_random_button_style()
    s3, e3 = get_random_button_style()
    buttons = [
        [InlineKeyboardButton("➕ Add Extra Days", callback_data=f"add_days_{user_id}", icon_custom_emoji_id=e1, style=s1)],
        [InlineKeyboardButton("➖ Remove Premium", callback_data=f"rem_prem_{user_id}", icon_custom_emoji_id=e2, style=s2)],
        [InlineKeyboardButton("🔙 Back", callback_data="back_to_list_prem", icon_custom_emoji_id=e3, style=s3)]
    ]

    await query.message.edit(text, reply_markup=InlineKeyboardMarkup(buttons))

@Bot.on_callback_query(filters.regex(r"^add_days_(\d+)"))
async def add_days_callback(client, query: CallbackQuery):
    user_id = int(query.data.split("_")[-1])

    await query.answer()
    try:
        ask_days = await query.message.chat.ask(f"<b>Please Enter the number of EXTRA days to add for user <code>{user_id}</code>:</b>", filters=filters.text, timeout=60)
        try:
            days = int(ask_days.text)
        except ValueError:
            return await ask_days.reply("<b>❌ Invalid value. Aborted.</b>")

        expiry = await add_premium(user_id, days, 'd')
        await ask_days.reply(f"<b>✅ Added {days} days to <code>{user_id}</code>. New Expiry: {expiry}</b>")
    except Exception as e:
        await query.message.reply(f"<b>❌ Error:</b> <code>{e}</code>")

@Bot.on_callback_query(filters.regex(r"^rem_prem_(\d+)"))
async def rem_prem_callback(client, query: CallbackQuery):
    user_id = int(query.data.split("_")[-1])
    await remove_premium(user_id)
    await query.answer("✅ Premium Removed", show_alert=True)
    # Go back to list
    users = await get_all_premium_users()
    count = len(users)
    text = f"<b>⚡ PREMIUM USERS LIST ⚡</b>\n\nTotal Premium Users: <code>{count}</code>\n\nSelect a user to manage:"
    buttons = []
    for user in users:
        u_id = user['user_id']
        try:
            u_info = await client.get_users(u_id)
            name = u_info.first_name
        except: name = "Unknown"
        rem_days = int(user['remaining_seconds'] // (24 * 3600))
        s, e = get_random_button_style()
        buttons.append([InlineKeyboardButton(f"👤 {name} ({u_id}) - {rem_days}d", callback_data=f"manage_prem_{u_id}", icon_custom_emoji_id=e, style=s)])
    s, e = get_random_button_style()
    buttons.append([InlineKeyboardButton("❌ Close", callback_data="close", icon_custom_emoji_id=e, style=s)])
    await query.message.edit(text, reply_markup=InlineKeyboardMarkup(buttons))

@Bot.on_callback_query(filters.regex("^back_to_list_prem$"))
async def back_to_list_prem_callback(client, query: CallbackQuery):
    users = await get_all_premium_users()
    count = len(users)
    text = f"<b>⚡ PREMIUM USERS LIST ⚡</b>\n\nTotal Premium Users: <code>{count}</code>\n\nSelect a user to manage:"
    buttons = []
    for user in users:
        u_id = user['user_id']
        try:
            u_info = await client.get_users(u_id)
            name = u_info.first_name
        except: name = "Unknown"
        rem_days = int(user['remaining_seconds'] // (24 * 3600))
        s, e = get_random_button_style()
        buttons.append([InlineKeyboardButton(f"👤 {name} ({u_id}) - {rem_days}d", callback_data=f"manage_prem_{u_id}", icon_custom_emoji_id=e, style=s)])
    s, e = get_random_button_style()
    buttons.append([InlineKeyboardButton("❌ Close", callback_data="close", icon_custom_emoji_id=e, style=s)])
    await query.message.edit(text, reply_markup=InlineKeyboardMarkup(buttons))
