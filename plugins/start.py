# Don't Remove Credit @ALONEKINGSTAR77, @ALONEKINGSTAR77
# Ask Doubt on telegram @ALONEKINGSTAR77Support
#
# Copyright (C) 2025 by @ALONEKINGSTAR77@Github, < https://github.com/@ALONEKINGSTAR77 >.
#
# This file is part of < https://github.com/@ALONEKINGSTAR77/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/@ALONEKINGSTAR77/FileStore/blob/master/LICENSE >
#
# All rights reserved.
#

import asyncio
import random
import uuid
import logging
import time
from datetime import datetime, timedelta
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode, ChatAction, ButtonStyle
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, ChatInviteLink, ChatPrivileges
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, UserNotParticipant
from pytz import timezone
from bot import Bot
from config import *
from helper_func import is_subscribed, decode, get_messages, send_media, get_exp_time, get_readable_time, is_sub, admin, check_admin, get_random_button_style, CHAT_INFO_CACHE, TG_SEMA
from database.database import db
from database.db_premium import is_premium_user, collection, add_premium, remove_premium, check_user_plan


BAN_SUPPORT = f"{BAN_SUPPORT}"
TUT_VID = f"{TUT_VID}"

async def short_url(client: Client, message: Message, base64_string):
    try:
        user_id = message.from_user.id
        # Generate a unique token for verification (with prefix to avoid overlap)
        verify_token = f"v_{str(uuid.uuid4())}"
        await db.add_verify_token(verify_token, user_id, base64_string)

        # Start the verification flow at the Task Page
        base_url = f"https://{URL}" if not URL.startswith("http") else URL
        hidden_link = f"{base_url}/task/{verify_token}"

        s1, e1 = get_random_button_style()
        s2, e2 = get_random_button_style()
        s3, e3 = get_random_button_style()

        is_tutorial = await db.get_setting("is_tutorial", True)
        buttons = [
            [
                InlineKeyboardButton(text="ᴅᴏᴡɴʟᴏᴀᴅ", url=hidden_link, icon_custom_emoji_id=e1, style=s1)
            ]
        ]
        if is_tutorial:
            buttons[0].append(InlineKeyboardButton(text="ᴛᴜᴛᴏʀɪᴀʟ", url=TUT_VID, icon_custom_emoji_id=e2, style=s2))

        await send_media(
            message=message,
            media=random.choice(PICS),
            caption=SHORT_MSG.format(),
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    except IndexError:
        pass


@Bot.on_message(filters.command('start') & filters.private)
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or "N/A"
    is_premium = await is_premium_user(user_id)
    is_admin = await check_admin(None, client, message)
    is_direct = False
    base64_string = None

    # Add user if not already present
    if not await db.present_user(user_id):
        try:
            await db.add_user(user_id)
        except:
            pass

    # Check Maintenance Mode
    maintenance_expiry = await db.get_maintenance()
    if maintenance_expiry and maintenance_expiry > datetime.now() and not is_admin:
        remaining = (maintenance_expiry - datetime.now()).total_seconds()
        s, e = get_random_button_style()
        return await message.reply_text(
            "<b>✧─── [ 🛠️ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ ᴍᴏᴅᴇ 🛠️ ] ───✧</b>\n\n"
            "<b>👋 ʜᴇʟʟᴏ {mention}!</b>\n\n"
            "<b><blockquote>⚠️ sᴏʀʀʏ, ᴛʜᴇ ʙᴏᴛ ɪs ᴄᴜʀʀᴇɴᴛʟʏ ᴜɴᴅᴇʀ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ ᴛᴏ ɪᴍᴘʀᴏᴠᴇ ᴏᴜʀ sᴇʀᴠɪᴄᴇs. ʙᴏᴛ ᴡɪʟʟ ʙᴇ ʙᴀᴄᴋ ɪɴ {time}.</blockquote></b>\n\n"
            "<i>✨ Pʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ. Tʜᴀɴᴋ ʏᴏᴜ ғᴏʀ ʏᴏᴜʀ ᴘᴀᴛɪᴇɴᴄᴇ! 💎</i>".format(
                mention=message.from_user.mention,
                time=get_readable_time(int(remaining))
            ),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✨ ᴊᴏɪɴ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ ✧", url="https://t.me/ALONEKINGSTAR77", icon_custom_emoji_id=e, style=s)]])
        )

    # Check if user is banned (Early exit)
    if await db.ban_user_exist(user_id):
        s, e = get_random_button_style()
        return await message.reply_text(
            "<b>✧─── [ 🚫 ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ 🚫 ] ───✧</b>\n\n"
            "<b><blockquote>⛔️ You are Bᴀɴɴᴇᴅ from using this bot.</blockquote></b>\n\n"
            "<i>✨ Contact support if you think this is a mistake. ✧</i>",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("💎 Contact Support", url=BAN_SUPPORT, icon_custom_emoji_id=e, style=s)]]
            )
        )

    # ✅ Check Force Subscription
    if not await is_subscribed(client, user_id):
        return await not_joined(client, message)

    # File auto-delete time in seconds
    FILE_AUTO_DELETE = await db.get_del_timer()

    # Handle normal message flow
    text = message.text

    if len(text) > 7:
        try:
            basic = text.split(" ", 1)[1]

            # Direct Link Bypass
            if basic.startswith("direct_"):
                base64_string = basic[7:]
                is_direct = True

            # Token Based Verification Check
            elif basic.strip().startswith("v_"):
                token = basic.strip()
                token_data = await db.get_verify_token(token)

                if not token_data:
                    logging.warning(f"Verification token not found: {token} for user {user_id}")
                    return await message.reply_text("<b>❌ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ᴇxᴘɪʀᴇᴅ ᴏʀ ɪɴᴠᴀʟɪᴅ. ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ғʀᴏᴍ ᴛʜᴇ ʟɪɴᴋ.</b>")

                if token_data['user_id'] != user_id:
                    logging.warning(f"User ID mismatch for token {token}: expected {token_data['user_id']}, got {user_id}")
                    return await message.reply_text("<b>❌ ᴛʜɪs ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ʟɪɴᴋ ᴡᴀs ɴᴏᴛ ɢᴇɴᴇʀᴀᴛᴇᴅ ғᴏʀ ʏᴏᴜ. ᴘʟᴇᴀsᴇ ɢᴇɴᴇʀᴀᴛᴇ ʏᴏᴜʀ ᴏᴡɴ ʟɪɴᴋ.</b>")

                # Check if multi-stage verification is complete
                if token_data.get('status') != 'verified':
                    logging.warning(f"Token {token} found but not fully verified. Status: {token_data.get('status')}")
                    return await message.reply_text("<b>❌ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ɪɴᴄᴏᴍᴘʟᴇᴛᴇ. ᴘʟᴇᴀsᴇ ᴄᴏᴍᴘʟᴇᴛᴇ ᴀʟʟ sᴛᴇᴘs!</b>")

                logging.info(f"Verification successful for user {user_id} with token {token}")
                base64_string = token_data['payload']
                is_direct = True
                await db.delete_verify_token(token)

            else:
                base64_string = basic
                # Check if shortlinks are globally disabled or not configured
                shortener_enabled = await db.get_shortener_status()
                if not SHORTLINK_URL or not SHORTLINK_API or SHORTLINK_URL.lower() == "none" or not shortener_enabled:
                    is_direct = True
                else:
                    is_direct = False

            if not is_premium and user_id != OWNER_ID and not is_direct:
                # Check for 24h verification persistence
                verify_status = await db.get_verify_status(user_id)
                last_verified = verify_status.get('verified_time', 0)
                if time.time() - last_verified < 86400: # 24 hours
                    is_direct = True
                else:
                    await short_url(client, message, base64_string)
                    return

        except Exception as e:
            print(f"Error processing start payload: {e}")
            return

        if not base64_string:
            return

        await db.track_link_click(base64_string)
        string = decode(base64_string)
        argument = string.split("-")

        ids = []
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
                ids = range(start, end + 1) if start <= end else list(range(start, end - 1, -1))
            except Exception as e:
                print(f"Error decoding IDs: {e}")
                return

        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except Exception as e:
                print(f"Error decoding ID: {e}")
                return

        temp_msg = await message.reply("<b>Please wait...</b>")
        try:
            messages = await get_messages(client, ids)
        except Exception as e:
            await message.reply_text("Something went wrong!")
            print(f"Error getting messages: {e}")
            return
        finally:
            await temp_msg.delete()

        fsub_msgs = []
        for msg in messages:
            if not msg or msg.empty:
                continue
            original_caption = msg.caption.html if msg.caption else ""
            prefix = "<b>@OTAKUSTARTELUGU</b>\n\n"
            caption = f"{prefix}{original_caption}\n\n{CUSTOM_CAPTION}" if CUSTOM_CAPTION else f"{prefix}{original_caption}"
            reply_markup = msg.reply_markup if DISABLE_CHANNEL_BUTTON else None
            try:
                snt = await msg.copy(
                    chat_id=message.from_user.id,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup,
                    protect_content=PROTECT_CONTENT
                )
                fsub_msgs.append(snt)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                snt = await msg.copy(
                    chat_id=message.from_user.id,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup,
                    protect_content=PROTECT_CONTENT
                )
                fsub_msgs.append(snt)
            except Exception:
                pass


        if FILE_AUTO_DELETE > 0:
            notification_msg = await message.reply(
                f"<b>Tʜɪs Fɪʟᴇ ᴡɪʟʟ ʙᴇ Dᴇʟᴇᴛᴇᴅ ɪɴ  {get_exp_time(FILE_AUTO_DELETE)}. Pʟᴇᴀsᴇ sᴀᴠᴇ ᴏʀ ғᴏʀᴡᴀʀᴅ ɪᴛ ᴛᴏ ʏᴏᴜʀ sᴀᴠᴇᴅ ᴍᴇssᴀɢᴇs ʙᴇғᴏʀᴇ ɪᴛ ɢᴇᴛs Dᴇʟᴇᴛᴇᴅ.</b>"
            )

            await asyncio.sleep(FILE_AUTO_DELETE)

            for snt_msg in fsub_msgs:
                if snt_msg:
                    try:    
                        await snt_msg.delete()  
                    except Exception as e:
                        print(f"Error deleting message {snt_msg.id}: {e}")

            try:
                reload_url = (
                    f"https://t.me/{client.username}?start={message.command[1]}"
                    if message.command and len(message.command) > 1
                    else None
                )
                s, e = get_random_button_style()
                keyboard = InlineKeyboardMarkup(
                    [[InlineKeyboardButton("ɢᴇᴛ ғɪʟᴇ ᴀɢᴀɪɴ!", url=reload_url, icon_custom_emoji_id=e, style=s)]]
                ) if reload_url else None

                await notification_msg.edit(
                    "<b>✧─── [ 🗑️ ғɪʟᴇ ᴅᴇʟᴇᴛᴇᴅ 🗑️ ] ───✧</b>\n\n"
                    "<b><blockquote>ʏᴏᴜʀ ᴠɪᴅᴇᴏ / ꜰɪʟᴇ ɪꜱ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ !!</blockquote></b>\n\n"
                    "<b>✨ ᴄʟɪᴄᴋ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ ɪᴛ ᴀɢᴀɪɴ 👇 ✧</b>",
                    reply_markup=keyboard
                )
            except Exception as e:
                print(f"Error updating notification with 'Get File Again' button: {e}")
    else:
        s1, e1 = get_random_button_style()
        s2, e2 = get_random_button_style()
        s3, e3 = get_random_button_style()
        s4, e4 = get_random_button_style()
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🏯 Community", url=MAIN_LINK, icon_custom_emoji_id=e1, style=s1),
                    InlineKeyboardButton("⚡ Updates", url="https://t.me/ALONEKINGSTAR77", icon_custom_emoji_id=e2, style=s2)
                ],
                [
                    InlineKeyboardButton("🌸 About", callback_data="about", icon_custom_emoji_id=e3, style=s3),
                    InlineKeyboardButton("⭐ Help", callback_data="help", icon_custom_emoji_id=e4, style=s4)
                ]
            ]
        )
        await send_media(
            message=message,
            media=random.choice(PICS),
            caption=START_MSG.format(
                mention=message.from_user.mention,
                bot_name=BOT_NAME
            ),
            reply_markup=reply_markup
        )
        
        return



#=====================================================================================##
# Don't Remove Credit @ALONEKINGSTAR77, @ALONEKINGSTAR77
# Ask Doubt on telegram @ALONEKINGSTAR77Support



async def not_joined(client: Client, message: Message):
    user_id = message.from_user.id
    now = time.time()

    # Check all channels
    all_channels = await db.show_channels()
    if not all_channels:
        return True

    check_tasks = [is_sub(client, user_id, cid) for cid in all_channels]
    sub_results = await asyncio.gather(*check_tasks)

    buttons = []
    for i, is_joined in enumerate(sub_results):
        if not is_joined:
            chat_id = all_channels[i]
            try:
                mode = await db.get_channel_mode(chat_id)
                # Cache chat info
                if chat_id in CHAT_INFO_CACHE and (now - CHAT_INFO_CACHE[chat_id][1] < 3600):
                    data = CHAT_INFO_CACHE[chat_id][0]
                else:
                    async with TG_SEMA:
                        chat = await client.get_chat(chat_id)
                    try:
                        link = chat.invite_link or await client.export_chat_invite_link(chat.id)
                    except:
                        link = f"https://t.me/{chat.username}" if chat.username else f"https://t.me/c/{str(chat.id)[4:]}"
                    data = {'title': chat.title, 'link': link}
                    CHAT_INFO_CACHE[chat_id] = (data, now)

                name = data['title']
                link = data['link']

                if mode == "on":
                    async with TG_SEMA:
                        invite = await client.create_chat_invite_link(
                            chat_id=chat_id,
                            creates_join_request=True,
                            expire_date=datetime.utcnow() + timedelta(seconds=FSUB_LINK_EXPIRY) if FSUB_LINK_EXPIRY else None
                        )
                    link = invite.invite_link

                s, e = get_random_button_style()
                buttons.append([InlineKeyboardButton(text=name, url=link, icon_custom_emoji_id=e, style=s)])

            except Exception as e:
                logging.error(f"Error with chat {chat_id}: {e}")

    if not buttons:
        return True

    # Generate Retry Button
    try:
        payload = message.command[1] if len(message.command) > 1 else ""
        if payload:
            s, e = get_random_button_style()
            buttons.append([
                InlineKeyboardButton(
                    text='♻️ Tʀʏ Aɢᴀɪɴ',
                    url=f"https://t.me/{client.username}?start={payload}",
                    icon_custom_emoji_id=e,
                    style=s
                )
            ])
    except Exception:
        pass

    await send_media(
        message=message,
        media=random.choice(PICS),
        caption=FORCE_MSG.format(
            mention=message.from_user.mention
        ),
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    return False

#=====================================================================================##

@Bot.on_message(filters.command('myplan') & filters.private)
async def check_plan(client: Client, message: Message):
    user_id = message.from_user.id  # Get user ID from the message

    # Get the premium status of the user
    status_message = await check_user_plan(user_id)

    # Send the response message to the user
    await message.reply(status_message)

#=====================================================================================##

@Bot.on_message(filters.command("count") & filters.private & admin)
async def total_verify_count_cmd(client, message: Message):
    total = await db.get_total_verify_count()
    await message.reply_text(f"Tᴏᴛᴀʟ ᴠᴇʀɪғɪᴇᴅ ᴛᴏᴋᴇɴs ᴛᴏᴅᴀʏ: <b>{total}</b>")


#=====================================================================================##

@Bot.on_message(filters.command('commands') & filters.private & admin)
async def bcmd(bot: Bot, message: Message):
    s, e = get_random_button_style()
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("• ᴄʟᴏsᴇ •", callback_data = "close", icon_custom_emoji_id=e, style=s)]])
    await message.reply(text=CMD_TXT, reply_markup = reply_markup)
