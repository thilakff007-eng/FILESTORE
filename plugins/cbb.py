#
# Copyright (C) 2025 by @ALONEKINGSTAR77@Github, < https://github.com/@ALONEKINGSTAR77 >.
#
# This file is part of < https://github.com/@ALONEKINGSTAR77/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/@ALONEKINGSTAR77/FileStore/blob/master/LICENSE >
#
# All rights reserved.

import random
from pyrogram import Client 
from bot import Bot
from config import *
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.database import *

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data

    if data == "help":
        await query.answer("✨ Opening Help Menu... ✧", show_alert=False)
        await query.message.edit_text(
            text=HELP_TXT.format(
                mention=query.from_user.mention,
                bot_name=BOT_NAME,
                main_link=MAIN_LINK
            ),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton('✨ ʜᴏᴍᴇ', callback_data='start'),
                 InlineKeyboardButton("🌸 ᴄʟᴏꜱᴇ", callback_data='close')]
            ])
        )

    elif data == "about":
        await query.answer("🌸 Opening About Menu... ✧", show_alert=False)
        await query.message.edit_text(
            text=ABOUT_TXT.format(
                bot_name=BOT_NAME,
                owner_name=OWNER,
                bot_username=client.username,
                main_link=MAIN_LINK
            ),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton('✨ ʜᴏᴍᴇ', callback_data='start'),
                 InlineKeyboardButton('🌸 ᴄʟᴏꜱᴇ', callback_data='close')]
            ])
        )

    elif data == "start":
        await query.answer("⚡ Welcome Back! ✧", show_alert=False)
        await query.message.edit_text(
            text=START_MSG.format(
                mention=query.from_user.mention,
                bot_name=BOT_NAME
            ),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🏯 ᴄᴏᴍᴍᴜɴɪᴛʏ", url=MAIN_LINK),
                        InlineKeyboardButton("⚡ ᴜᴘᴅᴀᴛᴇs", url="https://t.me/ALONEKINGSTAR77")
                    ],
                    [
                        InlineKeyboardButton("🌸 ᴀʙᴏᴜᴛ", callback_data="about"),
                        InlineKeyboardButton("⭐ ʜᴇʟᴘ", callback_data="help")
                    ],
                    [
                        InlineKeyboardButton("💎 ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇss 💎", callback_data="premium")
                    ]
                ]
            )
        )


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


    elif data == "premium":
        await query.answer("💎 Unlock Premium Features! ✧", show_alert=False)
        await query.message.delete()
        media = random.choice(PICS)
        caption = (
                f"✧─── [ 💎 ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴs 💎 ] ───✧\n\n"
                f"👋 ʜᴇʟʟᴏ {query.from_user.mention}!\n"
                f"🎖️ ᴀᴠᴀɪʟᴀʙʟᴇ ᴇxᴄʟᴜsɪᴠᴇ ᴘʟᴀɴs:\n\n"
                f"● ✨ {PRICE1} - 0 ᴅᴀʏs ᴛʀɪᴀʟ\n"
                f"● ✨ {PRICE2} - 1 ᴍᴏɴᴛʜ ᴘʀɪᴍᴇ\n"
                f"● ✨ {PRICE3} - 3 ᴍᴏɴᴛʜs ᴘʀɪᴍᴇ\n"
                f"● ✨ {PRICE4} - 6 ᴍᴏɴᴛʜs ᴘʀɪᴍᴇ\n"
                f"● ✨ {PRICE5} - 1 ʏᴇᴀʀ ᴘʀɪᴍᴇ\n\n"
                f"<b>💵 ᴘᴀʏ ᴠɪᴀ ᴜᴘɪ ɪᴅ:</b> <code>{UPI_ID}</code>\n\n"
                f"<b>♻️ ɪɴsᴛᴀɴᴛ ᴀᴄᴛɪᴠᴀᴛɪᴏɴ ᴀғᴛᴇʀ ᴘᴀʏᴍᴇɴᴛ.</b>\n"
                f"‼️ sᴇɴᴅ sᴄʀᴇᴇɴsʜᴏᴛ ᴛᴏ ᴀᴅᴍɪɴ ғᴏʀ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ. ✧"
            )
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "👨‍💻 ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ", url=(SCREENSHOT_URL)
                    )
                ],
                [InlineKeyboardButton("🌸 ᴄʟᴏsᴇ", callback_data="close")],
            ]
        )

        if media.endswith(('.mp4', '.mkv', '.webm')):
            await client.send_video(
                chat_id=query.message.chat.id,
                video=media,
                caption=caption,
                reply_markup=reply_markup
            )
        else:
            await client.send_photo(
                chat_id=query.message.chat.id,
                photo=media,
                caption=caption,
                reply_markup=reply_markup
            )



    elif data == "close":
        await query.answer()
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass

    elif data.startswith("rfs_ch_"):
        await query.answer()
        cid = int(data.split("_")[2])
        try:
            chat = await client.get_chat(cid)
            mode = await db.get_channel_mode(cid)
            status = "🟢 ᴏɴ" if mode == "on" else "🔴 ᴏғғ"
            new_mode = "ᴏғғ" if mode == "on" else "on"
            buttons = [
                [InlineKeyboardButton(f"ʀᴇǫ ᴍᴏᴅᴇ {'OFF' if mode == 'on' else 'ON'}", callback_data=f"rfs_toggle_{cid}_{new_mode}")],
                [InlineKeyboardButton("‹ ʙᴀᴄᴋ", callback_data="fsub_back")]
            ]
            await query.message.edit_text(
                f"Channel: {chat.title}\nCurrent Force-Sub Mode: {status}",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        except Exception:
            await query.answer("Failed to fetch channel info", show_alert=True)

    elif data.startswith("rfs_toggle_"):
        cid, action = data.split("_")[2:]
        cid = int(cid)
        mode = "on" if action == "on" else "off"

        await db.set_channel_mode(cid, mode)
        await query.answer(f"Force-Sub set to {'ON' if mode == 'on' else 'OFF'}")

        # Refresh the same channel's mode view
        chat = await client.get_chat(cid)
        status = "🟢 ON" if mode == "on" else "🔴 OFF"
        new_mode = "off" if mode == "on" else "on"
        buttons = [
            [InlineKeyboardButton(f"ʀᴇǫ ᴍᴏᴅᴇ {'OFF' if mode == 'on' else 'ON'}", callback_data=f"rfs_toggle_{cid}_{new_mode}")],
            [InlineKeyboardButton("‹ ʙᴀᴄᴋ", callback_data="fsub_back")]
        ]
        await query.message.edit_text(
            f"Channel: {chat.title}\nCurrent Force-Sub Mode: {status}",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    elif data == "fsub_back":
        await query.answer()
        channels = await db.show_channels()

        async def get_fsub_btn(cid):
            try:
                chat = await client.get_chat(cid)
                mode = await db.get_channel_mode(cid)
                status = "🟢" if mode == "on" else "🔴"
                return [InlineKeyboardButton(f"{status} {chat.title}", callback_data=f"rfs_ch_{cid}")]
            except:
                return None

        buttons = await asyncio.gather(*[get_fsub_btn(cid) for cid in channels])
        buttons = [b for b in buttons if b]

        await query.message.edit_text(
            "sᴇʟᴇᴄᴛ ᴀ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴛᴏɢɢʟᴇ ɪᴛs ғᴏʀᴄᴇ-sᴜʙ ᴍᴏᴅᴇ:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )


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
