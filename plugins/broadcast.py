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
import os
import random
import sys
import time
from datetime import datetime, timedelta
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode, ChatAction
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, ChatInviteLink, ChatPrivileges
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, UserNotParticipant
from bot import Bot
from config import *
from helper_func import admin, get_random_button_style
from database.database import db


#=====================================================================================##

REPLY_ERROR = "<code>Use this command as a reply to any telegram message without any spaces.</code>"

#=====================================================================================##


@Bot.on_message(filters.private & filters.command('pbroadcast') & admin)
async def send_pin_text(client: Bot, message: Message):
    if message.reply_to_message:
        all_users = db.user_data.find({})
        broadcast_msg = message.reply_to_message
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0

        sem = asyncio.Semaphore(10)

        async def do_pbroadcast(chat_id):
            nonlocal successful, blocked, deleted, unsuccessful
            async with sem:
                try:
                    sent_msg = await broadcast_msg.copy(chat_id)
                    await client.pin_chat_message(chat_id=chat_id, message_id=sent_msg.id, both_sides=True)
                    successful += 1
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    sent_msg = await broadcast_msg.copy(chat_id)
                    await client.pin_chat_message(chat_id=chat_id, message_id=sent_msg.id, both_sides=True)
                    successful += 1
                except UserIsBlocked:
                    await db.del_user(chat_id)
                    blocked += 1
                except InputUserDeactivated:
                    await db.del_user(chat_id)
                    deleted += 1
                except Exception:
                    unsuccessful += 1

        pls_wait = await message.reply("<i>ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴘʀᴏᴄᴇꜱꜱɪɴɢ....</i>")

        count = await db.count_users()
        batch = []
        async for user in all_users:
            batch.append(do_pbroadcast(user['_id']))
            if len(batch) >= 100:
                await asyncio.gather(*batch)
                batch = []
        if batch:
            await asyncio.gather(*batch)

        status = f"""<b><u>ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ</u></b>

Total Users: <code>{count}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code>"""

        s, e = get_random_button_style()
        return await pls_wait.edit(status, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("• ᴄʟᴏsᴇ •", callback_data="close", icon_custom_emoji_id=e, style=s)]]))

    else:
        msg = await message.reply("Reply to a message to broadcast and pin it.")
        await asyncio.sleep(8)
        await msg.delete()

#=====================================================================================##


@Bot.on_message(filters.private & filters.command('broadcast') & admin)
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        all_users = db.user_data.find({})
        broadcast_msg = message.reply_to_message
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0

        sem = asyncio.Semaphore(10) # 10 concurrent broadcasts

        async def do_broadcast(chat_id):
            nonlocal successful, blocked, deleted, unsuccessful
            async with sem:
                try:
                    await broadcast_msg.copy(chat_id)
                    successful += 1
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    await broadcast_msg.copy(chat_id)
                    successful += 1
                except UserIsBlocked:
                    await db.del_user(chat_id)
                    blocked += 1
                except InputUserDeactivated:
                    await db.del_user(chat_id)
                    deleted += 1
                except Exception:
                    unsuccessful += 1

        pls_wait = await message.reply("<i>ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴘʀᴏᴄᴇꜱꜱɪɴɢ....</i>")

        count = await db.count_users()
        batch = []
        async for user in all_users:
            batch.append(do_broadcast(user['_id']))
            if len(batch) >= 100:
                await asyncio.gather(*batch)
                batch = []
        if batch:
            await asyncio.gather(*batch)

        status = f"""<b><u>ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ</u>

Total Users: <code>{count}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""

        s, e = get_random_button_style()
        return await pls_wait.edit(status, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("• ᴄʟᴏsᴇ •", callback_data="close", icon_custom_emoji_id=e, style=s)]]))

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()

#=====================================================================================##
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

# broadcast with auto-del

@Bot.on_message(filters.private & filters.command('dbroadcast') & admin)
async def delete_broadcast(client: Bot, message: Message):
    if message.reply_to_message:
        try:
            duration = int(message.command[1])  # Get the duration in seconds
        except (IndexError, ValueError):
            await message.reply("<b>Pʟᴇᴀsᴇ ᴜsᴇ ᴀ ᴠᴀʟɪᴅ ᴅᴜʀᴀᴛɪᴏɴ ɪɴ sᴇᴄᴏɴᴅs.</b> Usᴀɢᴇ: /dbroadcast {duration}")
            return

        all_users = db.user_data.find({})
        broadcast_msg = message.reply_to_message
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0

        sem = asyncio.Semaphore(10)

        async def do_dbroadcast(chat_id):
            nonlocal successful, blocked, deleted, unsuccessful
            async with sem:
                try:
                    sent_msg = await broadcast_msg.copy(chat_id)
                    async def auto_delete():
                        await asyncio.sleep(duration)
                        try:
                            await sent_msg.delete()
                        except:
                            pass
                    asyncio.create_task(auto_delete())
                    successful += 1
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    sent_msg = await broadcast_msg.copy(chat_id)
                    async def auto_delete_flood():
                        await asyncio.sleep(duration)
                        try:
                            await sent_msg.delete()
                        except:
                            pass
                    asyncio.create_task(auto_delete_flood())
                    successful += 1
                except UserIsBlocked:
                    await db.del_user(chat_id)
                    blocked += 1
                except InputUserDeactivated:
                    await db.del_user(chat_id)
                    deleted += 1
                except Exception:
                    unsuccessful += 1

        pls_wait = await message.reply("<i>Broadcast with auto-delete processing....</i>")

        count = await db.count_users()
        batch = []
        async for user in all_users:
            batch.append(do_dbroadcast(user['_id']))
            if len(batch) >= 100:
                await asyncio.gather(*batch)
                batch = []
        if batch:
            await asyncio.gather(*batch)

        status = f"""<b><u>Bʀᴏᴀᴅᴄᴀsᴛɪɴɢ ᴡɪᴛʜ Aᴜᴛᴏ-Dᴇʟᴇᴛᴇ Cᴏᴍᴘʟᴇᴛᴇᴅ</u>

Total Users: <code>{count}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""

        s, e = get_random_button_style()
        return await pls_wait.edit(status, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("• ᴄʟᴏsᴇ •", callback_data="close", icon_custom_emoji_id=e, style=s)]]))

    else:
        msg = await message.reply("Pʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ʙʀᴏᴀᴅᴄᴀsᴛ ɪᴛ ᴡɪᴛʜ Aᴜᴛᴏ-Dᴇʟᴇᴛᴇ.")
        await asyncio.sleep(8)
        await msg.delete()


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