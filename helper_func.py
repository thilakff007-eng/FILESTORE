#(©)@ALONEKINGSTAR77
#@ALONEKINGSTAR77 on Tg #Dont remove this line

import base64
import re
import asyncio
import time
import random
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus, ButtonStyle
from config import *
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from shortzy import Shortzy
from pyrogram.errors import FloodWait
from database.database import db
from database.db_premium import is_premium_user

# Subscription Cache: (user_id, channel_id) -> (bool, timestamp)
SUB_CACHE = {}
CACHE_TIME_TRUE = 300 # 5 minutes for joined users
CACHE_TIME_FALSE = 10 # 10 seconds for non-joined users

# Channel List Cache
CHANNELS_CACHE = []
CHANNELS_CACHE_TS = 0
MODES_CACHE = {}
MODES_CACHE_TS = 0
ADMINS_CACHE = []
ADMINS_CACHE_TS = 0
CHAT_INFO_CACHE = {}

# Semaphore to limit concurrent TG API calls
TG_SEMA = asyncio.Semaphore(10)

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

#used for cheking if a user is admin ~Owner also treated as admin level
async def check_admin(filter, client, update):
    global ADMINS_CACHE, ADMINS_CACHE_TS
    try:
        user_id = update.from_user.id
        if user_id == OWNER_ID:
            return True

        now = time.time()
        if now - ADMINS_CACHE_TS > 60:
            ADMINS_CACHE = await db.get_all_admins()
            ADMINS_CACHE_TS = now

        return user_id in ADMINS_CACHE
    except Exception as e:
        print(f"! Exception in check_admin: {e}")
        return False


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

async def is_subscribed(client, user_id):
    global CHANNELS_CACHE, CHANNELS_CACHE_TS

    if user_id == OWNER_ID:
        return True

    # Premium users bypass everything
    if await is_premium_user(user_id):
        return True

    now = time.time()
    if now - CHANNELS_CACHE_TS > 60:
        CHANNELS_CACHE = await db.show_channels()
        CHANNELS_CACHE_TS = now

    channel_ids = CHANNELS_CACHE

    if not channel_ids:
        return True

    # Check all in parallel for speed
    tasks = [is_sub(client, user_id, cid) for cid in channel_ids]
    results = await asyncio.gather(*tasks)
    return all(results)


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

async def is_sub(client, user_id, channel_id):
    global MODES_CACHE, MODES_CACHE_TS
    # Check Cache
    now = time.time()
    if (user_id, channel_id) in SUB_CACHE:
        val, ts = SUB_CACHE[(user_id, channel_id)]
        cache_time = CACHE_TIME_TRUE if val else CACHE_TIME_FALSE
        if now - ts < cache_time:
            return val

    res = False
    try:
        async with TG_SEMA:
            member = await client.get_chat_member(channel_id, user_id)
            status = member.status
            res = status in {
                ChatMemberStatus.OWNER,
                ChatMemberStatus.ADMINISTRATOR,
                ChatMemberStatus.MEMBER
            }
    except UserNotParticipant:
        if now - MODES_CACHE_TS > 60:
            MODES_CACHE_TS = now

        if channel_id not in MODES_CACHE or now - MODES_CACHE.get(f"{channel_id}_ts", 0) > 60:
            mode = await db.get_channel_mode(channel_id)
            MODES_CACHE[channel_id] = mode
            MODES_CACHE[f"{channel_id}_ts"] = now
        else:
            mode = MODES_CACHE[channel_id]

        if mode == "on":
            res = await db.req_user_exist(channel_id, user_id)
        else:
            res = False
    except Exception as e:
        print(f"[!] Error in is_sub(): {e}")
        res = False

    SUB_CACHE[(user_id, channel_id)] = (res, now)
    return res

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


def encode(string):
    string_bytes = string.encode("ascii")
    base64_bytes = base64.urlsafe_b64encode(string_bytes)
    base64_string = (base64_bytes.decode("ascii")).strip("=")
    return base64_string

def decode(base64_string):
    base64_string = base64_string.strip("=") # links generated before this commit will be having = sign, hence striping them to handle padding errors.
    base64_bytes = (base64_string + "=" * (-len(base64_string) % 4)).encode("ascii")
    string_bytes = base64.urlsafe_b64decode(base64_bytes) 
    string = string_bytes.decode("ascii")
    return string

async def get_messages(client, message_ids):
    messages = []
    total_messages = 0
    while total_messages != len(message_ids):
        temb_ids = message_ids[total_messages:total_messages+200]
        try:
            msgs = await client.get_messages(
                chat_id=client.db_channel.id,
                message_ids=temb_ids
            )
        except FloodWait as e:
            await asyncio.sleep(e.x)
            msgs = await client.get_messages(
                chat_id=client.db_channel.id,
                message_ids=temb_ids
            )
        except:
            pass
        total_messages += len(temb_ids)
        messages.extend(msgs)
    return messages

async def get_message_id(client, message):
    if message.forward_origin:
        # Check for Chat origin (channels)
        if hasattr(message.forward_origin, "chat") and message.forward_origin.chat:
            if message.forward_origin.chat.id == client.db_channel.id:
                return getattr(message.forward_origin, "message_id", message.forward_from_message_id)
        return 0
    elif message.text:
        pattern = r"https://t.me/(?:c/)?(.*)/(\d+)"
        matches = re.match(pattern,message.text)
        if not matches:
            return 0
        channel_id = matches.group(1)
        msg_id = int(matches.group(2))
        if channel_id.isdigit():
            if f"-100{channel_id}" == str(client.db_channel.id):
                return msg_id
        else:
            if channel_id == client.db_channel.username:
                return msg_id
    else:
        return 0


def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    hmm = len(time_list)
    for x in range(hmm):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += f"{time_list.pop()}, "
    time_list.reverse()
    up_time += ":".join(time_list)
    return up_time


def get_exp_time(seconds):
    periods = [('days', 86400), ('hours', 3600), ('mins', 60), ('secs', 1)]
    result = ''
    for period_name, period_seconds in periods:
        if seconds >= period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            result += f'{int(period_value)} {period_name}'
    return result

def parse_time(time_str):
    # Parses time like 30m, 1h, 1d
    units = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
    time_str = time_str.lower().strip()

    # Handle 'min' as 'm'
    if time_str.endswith('min'):
        time_str = time_str[:-3] + 'm'

    try:
        if time_str[-1].isdigit():
            return int(time_str)

        number = int(time_str[:-1])
        unit = time_str[-1]
        return number * units.get(unit, 1)
    except:
        return None

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


async def get_shortlink(url, api, link):
    shortzy = Shortzy(api_key=api, base_site=url)
    link = await shortzy.convert(link)
    return link

async def send_media(message, media, caption, reply_markup=None):
    if media.endswith(('.mp4', '.mkv', '.webm')):
        try:
            return await message.reply_video(
                video=media,
                caption=caption,
                reply_markup=reply_markup
            )
        except Exception:
            return await message.reply_animation(
                animation=media,
                caption=caption,
                reply_markup=reply_markup
            )
    else:
        return await message.reply_photo(
            photo=media,
            caption=caption,
            reply_markup=reply_markup
        )

def get_random_button_style():
    styles = [ButtonStyle.PRIMARY, ButtonStyle.SUCCESS, ButtonStyle.DANGER]
    emojis = [5440389890787281213, 5355142851615283756, 5354968347094046619, 5411322049111827415, 5451996160375954443]
    return random.choice(styles), random.choice(emojis)

subscribed = filters.create(is_subscribed)
admin = filters.create(check_admin)

#@ALONEKINGSTAR77 on Tg :

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