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

@Bot.on_callback_query(filters.regex("^cp_toggle_shortener$"))
async def toggle_shortener_cb(client: Client, callback_query: CallbackQuery):
    if callback_query.from_user.id != OWNER_ID and not await db.admin_exist(callback_query.from_user.id):
        return await callback_query.answer("⚠️ Access Denied!", show_alert=True)

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
    await callback_query.answer(f"✅ Tutorial Button {'Enabled' if new_status else 'Disabled'}!")

@Bot.on_callback_query(filters.regex("^cp_toggle_protect$"))
async def toggle_protect_cb(client: Client, callback_query: CallbackQuery):
    if callback_query.from_user.id != OWNER_ID and not await db.admin_exist(callback_query.from_user.id):
        return await callback_query.answer("⚠️ Access Denied!", show_alert=True)

    current_status = await db.get_protect_content()
    new_status = not current_status
    await db.set_protect_content(new_status)

    await callback_query.message.edit_reply_markup(
        reply_markup=await get_control_panel_markup(client)
    )
    await callback_query.answer(f"✅ Content Protection {'Enabled' if new_status else 'Disabled'}!")

@Bot.on_callback_query(filters.regex("^cp_set_del_timer$"))
async def set_del_timer_cb(client: Client, callback_query: CallbackQuery):
    if callback_query.from_user.id != OWNER_ID and not await db.admin_exist(callback_query.from_user.id):
        return await callback_query.answer("Access Denied!", show_alert=True)

    await callback_query.answer("🕒 Update Auto-Delete Timer")

    try:
        timer_msg = await client.ask(
            chat_id=callback_query.from_user.id,
            text="<b>Please send the new Auto Delete Timer in seconds.</b>\n\n<i>Example: 600 for 10 minutes.</i>",
            timeout=60
        )
    except:
        return

    if not timer_msg.text:
         return await timer_msg.reply_text("❌ Invalid input!")

    try:
        new_timer = int(timer_msg.text)
        await db.set_del_timer(new_timer)
        await timer_msg.reply_text(f"✅ Auto Delete Timer updated to {new_timer} seconds.")
        await callback_query.message.edit_reply_markup(
            reply_markup=await get_control_panel_markup(client)
        )
    except ValueError:
        await timer_msg.reply_text("❌ Invalid input! Please send a number.")

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

@Bot.on_callback_query(filters.regex("^cp_manage_fsub$"))
async def manage_fsub_cb(client: Client, callback_query: CallbackQuery):
    if callback_query.from_user.id != OWNER_ID and not await db.admin_exist(callback_query.from_user.id):
        return await callback_query.answer("⚠️ Access Denied!", show_alert=True)
    await callback_query.answer("📢 Managing FSUB Channels")
    await callback_query.message.edit_text(
        "<b>✧─── [ 📢 ғsᴜʙ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ 🏯 ] ───✧</b>\n\n"
        "Manage your Force-Subscribe channels here. You can add, remove or toggle Request Mode for each channel.",
        reply_markup=await get_fsub_management_markup()
    )

@Bot.on_callback_query(filters.regex("^cp_add_fsub$"))
async def add_fsub_cb(client: Client, callback_query: CallbackQuery):
    if callback_query.from_user.id != OWNER_ID and not await db.admin_exist(callback_query.from_user.id):
        return await callback_query.answer("⚠️ Access Denied!", show_alert=True)
    await callback_query.answer("➕ Adding New Channel")

    try:
        ask_msg = await client.ask(
            chat_id=callback_query.from_user.id,
            text="<b>Forward a message from the channel or send the Channel ID (e.g., -100xxx).</b>\n\n<i>Make sure the bot is an admin in the channel!</i>",
            timeout=60
        )
    except:
        return

    if not ask_msg: return

    try:
        if ask_msg.forward_origin:
            if hasattr(ask_msg.forward_origin, "chat") and ask_msg.forward_origin.chat:
                chat_id = ask_msg.forward_origin.chat.id
            else:
                return await ask_msg.reply_text("❌ Could not determine channel ID from forward.")
        else:
            if not ask_msg.text:
                 return await ask_msg.reply_text("❌ Invalid Input!")
            try:
                chat_id = int(ask_msg.text)
            except:
                return await ask_msg.reply_text("❌ Invalid Input! Please send a valid numeric Channel ID.")

        all_chats = await db.show_channels()
        if chat_id in all_chats:
            return await ask_msg.reply_text("❌ This channel is already in the FSUB list.")

        try:
            chat = await client.get_chat(chat_id)
            bot_member = await client.get_chat_member(chat_id, "me")
            if bot_member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                 return await ask_msg.reply_text("❌ Bot must be an admin in the channel!")
        except Exception as e:
            return await ask_msg.reply_text(f"❌ Could not access channel: {e}")

        await db.add_channel(chat_id)
        await ask_msg.reply_text(f"✅ Successfully added <b>{chat.title}</b> to Force-Subscribe list.")
        await client.send_message(
            chat_id=callback_query.from_user.id,
            text="<b>✧─── [ 📢 ғsᴜʙ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ 🏯 ] ───✧</b>",
            reply_markup=await get_fsub_management_markup()
        )
    except Exception as e:
        logging.error(e)
        await ask_msg.reply_text(f"❌ Error: {e}")

@Bot.on_callback_query(filters.regex("^cp_rem_fsub$"))
async def rem_fsub_cb(client: Client, callback_query: CallbackQuery):
    if callback_query.from_user.id != OWNER_ID and not await db.admin_exist(callback_query.from_user.id):
        return await callback_query.answer("⚠️ Access Denied!", show_alert=True)
    await callback_query.answer("➖ Removing Channel")

    channels = await db.show_channels()
    if not channels:
        return await callback_query.message.edit_text("❌ No channels to remove.", reply_markup=await get_fsub_management_markup())

    try:
        ask_msg = await client.ask(
            chat_id=callback_query.from_user.id,
            text="<b>Send the Channel ID you want to remove.</b>\n\n<i>Use /fsublist to see current IDs.</i>",
            timeout=60
        )
    except:
        return

    if not ask_msg or not ask_msg.text:
         return

    try:
        chat_id = int(ask_msg.text)
        if chat_id not in channels:
            return await ask_msg.reply_text("❌ This ID is not in the FSUB list.")

        await db.rem_channel(chat_id)
        await ask_msg.reply_text(f"✅ Successfully removed channel <code>{chat_id}</code>.")
        await client.send_message(
            chat_id=callback_query.from_user.id,
            text="<b>✧─── [ 📢 ғsᴜʙ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ 🏯 ] ───✧</b>",
            reply_markup=await get_fsub_management_markup()
        )
    except ValueError:
        await ask_msg.reply_text("❌ Invalid Input! Please send a valid numeric Channel ID.")
    except Exception as e:
        await ask_msg.reply_text(f"❌ Error: {e}")
