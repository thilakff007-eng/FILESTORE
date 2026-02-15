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
import pytz
from datetime import datetime, timedelta
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode, ChatAction
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, ChatInviteLink, ChatPrivileges
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, UserNotParticipant
from bot import Bot
from config import *
from helper_func import admin, get_readable_time
from database.database import db

#=====================================================================================##

@Bot.on_message(filters.command('stats') & admin)
async def stats(bot: Bot, message: Message):
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)
    delta = now - bot.uptime
    uptime_str = get_readable_time(int(delta.total_seconds()))
    await message.reply(BOT_STATS_TEXT.format(uptime=uptime_str))


#=====================================================================================##

WAIT_MSG = "<b>Working....</b>"

#=====================================================================================##


@Bot.on_message(filters.command('users') & filters.private & admin)
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await db.full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")

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

#=====================================================================================##

#AUTO-DELETE

@Bot.on_message(filters.private & filters.command('dlt_time') & admin)
async def set_delete_time(client: Bot, message: Message):
    try:
        duration = int(message.command[1])

        await db.set_del_timer(duration)

        await message.reply(f"<b>Dᴇʟᴇᴛᴇ Tɪᴍᴇʀ ʜᴀs ʙᴇᴇɴ sᴇᴛ ᴛᴏ <blockquote>{duration} sᴇᴄᴏɴᴅs.</blockquote></b>")

    except (IndexError, ValueError):
        await message.reply("<b>Pʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴠᴀʟɪᴅ ᴅᴜʀᴀᴛɪᴏɴ ɪɴ sᴇᴄᴏɴᴅs.</b> Usage: /dlt_time {duration}")

@Bot.on_message(filters.private & filters.command('check_dlt_time') & admin)
async def check_delete_time(client: Bot, message: Message):
    duration = await db.get_del_timer()

    await message.reply(f"<b><blockquote>Cᴜʀʀᴇɴᴛ ᴅᴇʟᴇᴛᴇ ᴛɪᴍᴇʀ ɪs sᴇᴛ ᴛᴏ {duration}sᴇᴄᴏɴᴅs.</blockquote></b>")

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