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
from datetime import datetime, timedelta
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode, ChatAction
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, ChatInviteLink, ChatPrivileges
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, UserNotParticipant
from pytz import timezone
from bot import Bot
from config import *
from helper_func import is_subscribed, decode, get_messages, send_media, get_exp_time, get_readable_time, is_sub, admin, check_admin
from database.database import db
from database.db_premium import is_premium_user, collection, add_premium, remove_premium, check_user_plan


BAN_SUPPORT = f"{BAN_SUPPORT}"
TUT_VID = f"{TUT_VID}"

async def short_url(client: Client, message: Message, base64_string):
    try:
        # Hide shortlink using our own redirector domain
        base_url = f"https://{URL}" if not URL.startswith("http") else URL
        hidden_link = f"{base_url}/link/__{OWNER_ID}__/yu3elk{base64_string}7"

        buttons = [
            [
                InlineKeyboardButton(text="ᴅᴏᴡɴʟᴏᴀᴅ", url=hidden_link),
                InlineKeyboardButton(text="ᴛᴜᴛᴏʀɪᴀʟ", url=TUT_VID)
            ],
            [
                InlineKeyboardButton(text="ᴘʀᴇᴍɪᴜᴍ", callback_data="premium")
            ]
        ]

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
        return await message.reply_text(
            "<b>✧─── [ 🛠️ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ ᴍᴏᴅᴇ 🛠️ ] ───✧</b>\n\n"
            "<b>👋 ʜᴇʟʟᴏ {mention}!</b>\n\n"
            "<b><blockquote>⚠️ sᴏʀʀʏ, ᴛʜᴇ ʙᴏᴛ ɪs ᴄᴜʀʀᴇɴᴛʟʏ ᴜɴᴅᴇʀ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ ᴛᴏ ɪᴍᴘʀᴏᴠᴇ ᴏᴜʀ sᴇʀᴠɪᴄᴇs. ʙᴏᴛ ᴡɪʟʟ ʙᴇ ʙᴀᴄᴋ ɪɴ {time}.</blockquote></b>\n\n"
            "<i>✨ Pʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ. Tʜᴀɴᴋ ʏᴏᴜ ғᴏʀ ʏᴏᴜʀ ᴘᴀᴛɪᴇɴᴄᴇ! 💎</i>".format(
                mention=message.from_user.mention,
                time=get_readable_time(int(remaining))
            ),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✨ ᴊᴏɪɴ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ ✧", url="https://t.me/ALONEKINGSTAR77")]])
        )

    # Check if user is banned (Early exit)
    if await db.ban_user_exist(user_id):
        return await message.reply_text(
            "<b>✧─── [ 🚫 ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ 🚫 ] ───✧</b>\n\n"
            "<b><blockquote>⛔️ You are Bᴀɴɴᴇᴅ from using this bot.</blockquote></b>\n\n"
            "<i>✨ Contact support if you think this is a mistake. ✧</i>",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("💎 Contact Support", url=BAN_SUPPORT)]]
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
            if basic.startswith("direct_"):
                base64_string = basic[7:]
                is_direct = True
            elif basic.startswith("yu3elk"):
                base64_string = basic[6:-1]
                is_direct = True
            else:
                base64_string = basic
                is_direct = False

            if not is_premium and user_id != OWNER_ID and not is_direct:
                await short_url(client, message, base64_string)
                return

        except Exception as e:
            print(f"Error processing start payload: {e}")

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

        sem = asyncio.Semaphore(5) # Allow 5 concurrent copies

        async def copy_with_sem(msg):
            if not msg or msg.empty:
                return None
            async with sem:
                original_caption = msg.caption.html if msg.caption else ""
                caption = f"{original_caption}\n\n{CUSTOM_CAPTION}" if CUSTOM_CAPTION else original_caption
                reply_markup = msg.reply_markup if DISABLE_CHANNEL_BUTTON else None
                try:
                    return await msg.copy(
                        chat_id=message.from_user.id,
                        caption=caption,
                        parse_mode=ParseMode.HTML,
                        reply_markup=reply_markup,
                        protect_content=PROTECT_CONTENT
                    )
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    return await msg.copy(
                        chat_id=message.from_user.id,
                        caption=caption,
                        parse_mode=ParseMode.HTML,
                        reply_markup=reply_markup,
                        protect_content=PROTECT_CONTENT
                    )
                except Exception:
                    return None

        tasks = [copy_with_sem(msg) for msg in messages]
        snt_msgs = await asyncio.gather(*tasks)
        fsub_msgs = [m for m in snt_msgs if m]


        if FILE_AUTO_DELETE > 0:
            notification_msg = await message.reply(
                f"<b>Tʜɪs Fɪʟᴇ ᴡɪʟʟ ʙᴇ Dᴇʟᴇᴛᴇᴅ ɪɴ  {get_exp_time(FILE_AUTO_DELETE)}. Pʟᴇᴀsᴇ sᴀᴠᴇ ᴏʀ ғᴏʀᴡᴀʀᴅ ɪᴛ ᴛᴏ ʏᴏᴜʀ sᴀᴠᴇᴅ ᴍᴇssᴀɢᴇs ʙᴇғᴏʀᴇ ɪᴛ ɢᴇᴛs Dᴇʟᴇʟᴛᴇᴅ.</b>"
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
                keyboard = InlineKeyboardMarkup(
                    [[InlineKeyboardButton("ɢᴇᴛ ғɪʟᴇ ᴀɢᴀɪɴ!", url=reload_url)]]
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
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🏯 Community", url=MAIN_LINK),
                    InlineKeyboardButton("⚡ Updates", url="https://t.me/ALONEKINGSTAR77")
                ],
                [
                    InlineKeyboardButton("🌸 About", callback_data="about"),
                    InlineKeyboardButton("⭐ Help", callback_data="help")
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



# Create a global dictionary to store chat data
chat_data_cache = {}

async def not_joined(client: Client, message: Message):
    temp = await message.reply("<b><i>Checking Subscription...</i></b>")

    user_id = message.from_user.id
    buttons = []
    count = 0

    try:
        all_channels = await db.show_channels()  # Should return list of (chat_id, mode) tuples
        for total, chat_id in enumerate(all_channels, start=1):
            mode = await db.get_channel_mode(chat_id)  # fetch mode 

            await message.reply_chat_action(ChatAction.TYPING)

            if not await is_sub(client, user_id, chat_id):
                try:
                    # Cache chat info
                    if chat_id in chat_data_cache:
                        data = chat_data_cache[chat_id]
                    else:
                        data = await client.get_chat(chat_id)
                        chat_data_cache[chat_id] = data

                    name = data.title

                    # Generate proper invite link based on the mode
                    if mode == "on" and not data.username:
                        invite = await client.create_chat_invite_link(
                            chat_id=chat_id,
                            creates_join_request=True,
                            expire_date=datetime.utcnow() + timedelta(seconds=FSUB_LINK_EXPIRY) if FSUB_LINK_EXPIRY else None
                            )
                        link = invite.invite_link

                    else:
                        if data.username:
                            link = f"https://t.me/{data.username}"
                        else:
                            invite = await client.create_chat_invite_link(
                                chat_id=chat_id,
                                expire_date=datetime.utcnow() + timedelta(seconds=FSUB_LINK_EXPIRY) if FSUB_LINK_EXPIRY else None)
                            link = invite.invite_link

                    buttons.append([InlineKeyboardButton(text=name, url=link)])
                    count += 1
                    await temp.edit(f"<b>{'! ' * count}</b>")

                except Exception as e:
                    print(f"Error with chat {chat_id}: {e}")
                    return await temp.edit(
                        f"<b><i>! Eʀʀᴏʀ, Cᴏɴᴛᴀᴄᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ ᴛᴏ sᴏʟᴠᴇ ᴛʜᴇ ɪssᴜᴇs @ALONEKINGSTAR77</i></b>\n"
                        f"<blockquote expandable><b>Rᴇᴀsᴏɴ:</b> {e}</blockquote>"
                    )

        # Retry Button
        try:
            buttons.append([
                InlineKeyboardButton(
                    text='♻️ Tʀʏ Aɢᴀɪɴ',
                    url=f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ])
        except IndexError:
            pass

        await send_media(
            message=message,
            media=random.choice(PICS),
            caption=FORCE_MSG.format(
                mention=message.from_user.mention
            ),
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    except Exception as e:
        print(f"Final Error: {e}")
        await temp.edit(
            f"<b><i>! Eʀʀᴏʀ, Cᴏɴᴛᴀᴄᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ ᴛᴏ sᴏʟᴠᴇ ᴛʜᴇ ɪssᴜᴇs @ALONEKINGSTAR77</i></b>\n"
            f"<blockquote expandable><b>Rᴇᴀsᴏɴ:</b> {e}</blockquote>"
        )

#=====================================================================================##

@Bot.on_message(filters.command('myplan') & filters.private)
async def check_plan(client: Client, message: Message):
    user_id = message.from_user.id  # Get user ID from the message

    # Get the premium status of the user
    status_message = await check_user_plan(user_id)

    # Send the response message to the user
    await message.reply(status_message)

#=====================================================================================##
# Command to add premium user
@Bot.on_message(filters.command('addpremium') & filters.private & admin)
async def add_premium_user_command(client, msg):
    if len(msg.command) != 4:
        await msg.reply_text(
            "Usage: /addpremium <user_id> <time_value> <time_unit>\n\n"
            "Time Units:\n"
            "s - seconds\n"
            "m - minutes\n"
            "h - hours\n"
            "d - days\n"
            "y - years\n\n"
            "Examples:\n"
            "/addpremium 123456789 30 m → 30 minutes\n"
            "/addpremium 123456789 2 h → 2 hours\n"
            "/addpremium 123456789 1 d → 1 day\n"
            "/addpremium 123456789 1 y → 1 year"
        )
        return

    try:
        user_id = int(msg.command[1])
        time_value = int(msg.command[2])
        time_unit = msg.command[3].lower()  # supports: s, m, h, d, y

        # Call add_premium function
        expiration_time = await add_premium(user_id, time_value, time_unit)

        # Notify the admin
        await msg.reply_text(
            f"✅ User `{user_id}` added as a premium user for {time_value} {time_unit}.\n"
            f"Expiration Time: `{expiration_time}`"
        )

        # Notify the user
        await client.send_message(
            chat_id=user_id,
            text=(
                f"🎉 Premium Activated!\n\n"
                f"You have received premium access for `{time_value} {time_unit}`.\n"
                f"Expires on: `{expiration_time}`"
            ),
        )

    except ValueError:
        await msg.reply_text("❌ Invalid input. Please ensure user ID and time value are numbers.")
    except Exception as e:
        await msg.reply_text(f"⚠️ An error occurred: `{str(e)}`")


# Command to remove premium user
@Bot.on_message(filters.command('remove_premium') & filters.private & admin)
async def pre_remove_user(client: Client, msg: Message):
    if len(msg.command) != 2:
        await msg.reply_text("useage: /remove_premium user_id ")
        return
    try:
        user_id = int(msg.command[1])
        await remove_premium(user_id)
        await msg.reply_text(f"User {user_id} has been removed.")
    except ValueError:
        await msg.reply_text("user_id must be an integer or not available in database.")


# Command to list active premium users
@Bot.on_message(filters.command('premium_users') & filters.private & admin)
async def list_premium_users_command(client, message):
    # Define IST timezone
    ist = timezone("Asia/Kolkata")

    # Retrieve all users from the collection
    premium_users_cursor = collection.find({})
    premium_user_list = ['Active Premium Users in database:']
    current_time = datetime.now(ist)  # Get current time in IST

    # Use async for to iterate over the async cursor
    async for user in premium_users_cursor:
        user_id = user["user_id"]
        expiration_timestamp = user["expiration_timestamp"]

        try:
            # Convert expiration_timestamp to a timezone-aware datetime object in IST
            expiration_time = datetime.fromisoformat(expiration_timestamp).astimezone(ist)

            # Calculate remaining time
            remaining_time = expiration_time - current_time

            if remaining_time.total_seconds() <= 0:
                # Remove expired users from the database
                await collection.delete_one({"user_id": user_id})
                continue  # Skip to the next user if this one is expired

            # If not expired, retrieve user info
            user_info = await client.get_users(user_id)
            username = user_info.username if user_info.username else "No Username"
            first_name = user_info.first_name
            mention=user_info.mention

            # Calculate days, hours, minutes, seconds left
            days, hours, minutes, seconds = (
                remaining_time.days,
                remaining_time.seconds // 3600,
                (remaining_time.seconds // 60) % 60,
                remaining_time.seconds % 60,
            )
            expiry_info = f"{days}d {hours}h {minutes}m {seconds}s left"

            # Add user details to the list
            premium_user_list.append(
                f"UserID: <code>{user_id}</code>\n"
                f"User: @{username}\n"
                f"Name: {mention}\n"
                f"Expiry: {expiry_info}"
            )
        except Exception as e:
            premium_user_list.append(
                f"UserID: <code>{user_id}</code>\n"
                f"Error: Unable to fetch user details ({str(e)})"
            )

    if len(premium_user_list) == 1:  # No active users found
        await message.reply_text("I found 0 active premium users in my DB")
    else:
        await message.reply_text("\n\n".join(premium_user_list), parse_mode=None)


#=====================================================================================##

@Bot.on_message(filters.command("count") & filters.private & admin)
async def total_verify_count_cmd(client, message: Message):
    total = await db.get_total_verify_count()
    await message.reply_text(f"Tᴏᴛᴀʟ ᴠᴇʀɪғɪᴇᴅ ᴛᴏᴋᴇɴs ᴛᴏᴅᴀʏ: <b>{total}</b>")


#=====================================================================================##

@Bot.on_message(filters.command('commands') & filters.private & admin)
async def bcmd(bot: Bot, message: Message):        
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("• ᴄʟᴏsᴇ •", callback_data = "close")]])
    await message.reply(text=CMD_TXT, reply_markup = reply_markup, quote= True)
