#
# Copyright (C) 2025 by @ALONEKINGSTAR77@Github, < https://github.com/@ALONEKINGSTAR77 >.
#
# This file is part of < https://github.com/@ALONEKINGSTAR77/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/@ALONEKINGSTAR77/FileStore/blob/master/LICENSE >
#
# All rights reserved.

import random
import asyncio
import pytz
import logging
from datetime import datetime, timedelta
from pyrogram import Client, filters
from bot import Bot
from config import *
from pyrogram.enums import ButtonStyle
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, LinkPreviewOptions
from helper_func import get_random_button_style, get_readable_time, check_admin
from database.database import db
from database.db_premium import get_all_premium_users, add_premium, remove_premium

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    try:
        data = query.data
        user_id = query.from_user.id

        # Fast Admin Check
        is_admin = (user_id == OWNER_ID or await check_admin(None, client, query))

        # Check Maintenance Mode
        maintenance_expiry = await db.get_maintenance()
        if maintenance_expiry and maintenance_expiry > datetime.now() and not is_admin:
            return await query.answer("⚠️ Bot is under maintenance. Please try again later. ✧", show_alert=True)

        if data == "help":
            await query.answer("✨ Opening Help Menu... ✧")
            s1, e1 = get_random_button_style()
            s2, e2 = get_random_button_style()
            await query.message.edit_text(
                text=HELP_TXT.format(
                    mention=query.from_user.mention,
                    bot_name=BOT_NAME,
                    main_link=MAIN_LINK
                ),
                link_preview_options=LinkPreviewOptions(is_disabled=True),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton('✨ ʜᴏᴍᴇ', callback_data='start', icon_custom_emoji_id=e1, style=s1),
                     InlineKeyboardButton("🌸 ᴄʟᴏꜱᴇ", callback_data='close', icon_custom_emoji_id=e2, style=s2)]
                ])
            )

        elif data == "about":
            await query.answer("🌸 Opening About Menu... ✧")
            s1, e1 = get_random_button_style()
            s2, e2 = get_random_button_style()
            await query.message.edit_text(
                text=ABOUT_TXT.format(
                    bot_name=BOT_NAME,
                    owner_name=OWNER,
                    bot_username=client.username,
                    main_link=MAIN_LINK
                ),
                link_preview_options=LinkPreviewOptions(is_disabled=True),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton('✨ ʜᴏᴍᴇ', callback_data='start', icon_custom_emoji_id=e1, style=s1),
                     InlineKeyboardButton('🌸 ᴄʟᴏꜱᴇ', callback_data='close', icon_custom_emoji_id=e2, style=s2)]
                ])
            )

        elif data == "start":
            await query.answer("⚡ Welcome Back! ✧")
            s1, e1 = get_random_button_style()
            s2, e2 = get_random_button_style()
            s3, e3 = get_random_button_style()
            s4, e4 = get_random_button_style()
            s5, e5 = get_random_button_style()
            await query.message.edit_text(
                text=START_MSG.format(
                    mention=query.from_user.mention,
                    bot_name=BOT_NAME
                ),
                link_preview_options=LinkPreviewOptions(is_disabled=True),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🏯 ᴄᴏᴍᴍᴜɴɪᴛʏ", url=MAIN_LINK, icon_custom_emoji_id=e1, style=s1),
                            InlineKeyboardButton("⚡ ᴜᴘᴅᴀᴛᴇs", url="https://t.me/ALONEKINGSTAR77", icon_custom_emoji_id=e2, style=s2)
                        ],
                        [
                            InlineKeyboardButton("🌸 ᴀʙᴏᴜᴛ", callback_data="about", icon_custom_emoji_id=e3, style=s3),
                            InlineKeyboardButton("⭐ ʜᴇʟᴘ", callback_data="help", icon_custom_emoji_id=e4, style=s4)
                        ],
                        [
                            InlineKeyboardButton("💎 ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇss 💎", callback_data="premium", icon_custom_emoji_id=e5, style=s5)
                        ]
                    ]
                )
            )

        elif data == "premium":
            await query.answer("💎 Unlock Premium Features! ✧")
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
            s1, e1 = get_random_button_style()
            s2, e2 = get_random_button_style()
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "👨‍💻 ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ", url=(SCREENSHOT_URL), icon_custom_emoji_id=e1, style=s1
                        )
                    ],
                    [InlineKeyboardButton("🌸 ᴄʟᴏsᴇ", callback_data="close", icon_custom_emoji_id=e2, style=s2)],
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
                s1, e1 = get_random_button_style()
                s2, e2 = get_random_button_style()
                buttons = [
                    [InlineKeyboardButton(f"ʀᴇǫ ᴍᴏᴅᴇ {'OFF' if mode == 'on' else 'ON'}", callback_data=f"rfs_toggle_{cid}_{new_mode}", icon_custom_emoji_id=e1, style=s1)],
                    [InlineKeyboardButton("‹ ʙᴀᴄᴋ", callback_data="fsub_back", icon_custom_emoji_id=e2, style=s2)]
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
            s1, e1 = get_random_button_style()
            s2, e2 = get_random_button_style()
            buttons = [
                [InlineKeyboardButton(f"ʀᴇǫ ᴍᴏᴅᴇ {'OFF' if mode == 'on' else 'ON'}", callback_data=f"rfs_toggle_{cid}_{new_mode}", icon_custom_emoji_id=e1, style=s1)],
                [InlineKeyboardButton("‹ ʙᴀᴄᴋ", callback_data="fsub_back", icon_custom_emoji_id=e2, style=s2)]
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
                    s, e = get_random_button_style()
                    return [InlineKeyboardButton(f"{status} {chat.title}", callback_data=f"rfs_ch_{cid}", icon_custom_emoji_id=e, style=s)]
                except:
                    return None

            buttons = await asyncio.gather(*[get_fsub_btn(cid) for cid in channels])
            buttons = [b for b in buttons if b]

            s, e = get_random_button_style()
            buttons.append([InlineKeyboardButton("‹ ʙᴀᴄᴋ", callback_data="cp_back", icon_custom_emoji_id=e, style=s)])

            await query.message.edit_text(
                "sᴇʟᴇᴄᴛ ᴀ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴛᴏɢɢʟᴇ ɪᴛs ғᴏʀᴄᴇ-sᴜʙ ᴍᴏᴅᴇ:",
                reply_markup=InlineKeyboardMarkup(buttons)
            )

        elif data == "stats":
            if not is_admin:
                return await query.answer("⚠️ Access Denied!", show_alert=True)

            await query.answer("📊 Fetching statistics...")

            ist = pytz.timezone("Asia/Kolkata")
            now = datetime.now(ist)
            delta = now - client.uptime
            uptime_str = get_readable_time(int(delta.total_seconds()))

            users = await db.count_users()
            admins = await db.count_admins()
            from database.db_premium import get_premium_count
            premium = await get_premium_count()

            text = f"<b>✧─── [ ⚡ Bᴏᴛ Sᴛᴀᴛɪsᴛɪᴄs ⚡ ] ───✧</b>\n\n" \
                   f"<b>✨ Uᴘᴛɪᴍᴇ:</b> <code>{uptime_str}</code>\n" \
                   f"<b>👤 Tᴏᴛᴀʟ Usᴇʀs:</b> <code>{users}</code>\n" \
                   f"<b>💎 Pʀᴇᴍɪᴜᴍ Usᴇʀs:</b> <code>{premium}</code>\n" \
                   f"<b>🛠️ Tᴏᴛᴀʟ Aᴅᴍɪɴs:</b> <code>{admins}</code>\n\n" \
                   f"<i>⚡ Sᴛᴀᴛs Fᴇᴛᴄʜᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ! ✧</i>"

            s1, e1 = get_random_button_style()
            s2, e2 = get_random_button_style()

            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("‹ ʙᴀᴄᴋ", callback_data="cp_back", icon_custom_emoji_id=e1, style=s1)],
                [InlineKeyboardButton("• ᴄʟᴏsᴇ •", callback_data="close", icon_custom_emoji_id=e2, style=s2)]
            ])

            await query.message.edit_text(text, reply_markup=reply_markup)

        elif data == "cp_back":
            if not is_admin:
                return await query.answer("⚠️ Access Denied!", show_alert=True)
            await query.answer()
            from plugins.admin_panel import get_control_panel_markup
            await query.message.edit_text(
                "<b>✧─── [ ⚡ ᴀᴅᴍɪɴ ᴄᴏɴᴛʀᴏʟ ᴘᴀɴᴇʟ 🏯 ] ───✧</b>\n\n"
                "Welcome Senpai! Here you can manage all the bot's core variables and settings in real-time. ⭐",
                reply_markup=await get_control_panel_markup(client)
            )

        elif data.startswith("set_hash_"):
            if not is_admin:
                return await query.answer("⚠️ Access Denied!", show_alert=True)

            algo = data.split("_")[-1]
            await db.set_setting("primary_hash_algo", algo)
            await query.answer(f"✅ Set {algo} as primary hashing algorithm!", show_alert=True)

            current_algo = algo
            buttons = []
            for i in range(0, len(ALGORITHMS), 2):
                row = []
                for a in ALGORITHMS[i:i+2]:
                    prefix = "✅ " if a == current_algo else ""
                    row.append(InlineKeyboardButton(f"{prefix}{a}", callback_data=f"set_hash_{a}"))
                buttons.append(row)

            s, e = get_random_button_style()
            buttons.append([InlineKeyboardButton("• ᴄʟᴏsᴇ •", callback_data="close", icon_custom_emoji_id=e, style=s)])

            await query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))

        # Control Panel Toggles
        elif data == "cp_toggle_shortener":
            if not is_admin: return await query.answer("⚠️ Access Denied!", show_alert=True)
            status = await db.get_shortener_status()
            await db.set_shortener_status(not status)
            from plugins.admin_panel import get_control_panel_markup
            await query.message.edit_reply_markup(reply_markup=await get_control_panel_markup(client))
            await query.answer(f"✅ Shortener {'Disabled' if status else 'Enabled'}!")

        elif data == "cp_toggle_tutorial":
            if not is_admin: return await query.answer("⚠️ Access Denied!", show_alert=True)
            status = await db.get_setting("is_tutorial", True)
            await db.set_setting("is_tutorial", not status)
            from plugins.admin_panel import get_control_panel_markup
            await query.message.edit_reply_markup(reply_markup=await get_control_panel_markup(client))
            await query.answer(f"✅ Tutorial Button {'Disabled' if status else 'Enabled'}!")

        elif data == "cp_toggle_protect":
            if not is_admin: return await query.answer("⚠️ Access Denied!", show_alert=True)
            status = await db.get_protect_content()
            await db.set_protect_content(not status)
            from plugins.admin_panel import get_control_panel_markup
            await query.message.edit_reply_markup(reply_markup=await get_control_panel_markup(client))
            await query.answer(f"✅ Protection {'Disabled' if status else 'Enabled'}!")

        elif data == "cp_set_del_timer":
            if not is_admin: return await query.answer("⚠️ Access Denied!", show_alert=True)
            await query.answer("🕒 Send new timer in seconds")
            try:
                timer_msg = await client.ask(chat_id=user_id, text="<b>Send Auto-Delete timer (seconds):</b>", timeout=60)
                new_timer = int(timer_msg.text)
                await db.set_del_timer(new_timer)
                await timer_msg.reply(f"✅ Timer updated to {new_timer}s")
                from plugins.admin_panel import get_control_panel_markup
                await query.message.edit_reply_markup(reply_markup=await get_control_panel_markup(client))
            except: pass

        elif data == "cp_manage_fsub":
            if not is_admin: return await query.answer("⚠️ Access Denied!", show_alert=True)
            await query.answer()
            from plugins.admin_panel import get_fsub_management_markup
            await query.message.edit_text("<b>✧─── [ 📢 ғsᴜʙ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ 🏯 ] ───✧</b>", reply_markup=await get_fsub_management_markup())

        elif data == "cp_add_fsub":
            if not is_admin: return await query.answer("⚠️ Access Denied!", show_alert=True)
            await query.answer("➕ Adding Channel")
            try:
                ask = await client.ask(chat_id=user_id, text="<b>Forward a message or send Channel ID:</b>", timeout=60)
                if ask.forward_origin and hasattr(ask.forward_origin, "chat"):
                    cid = ask.forward_origin.chat.id
                else: cid = int(ask.text)
                await db.add_channel(cid)
                await ask.reply(f"✅ Added {cid}")
            except: pass

        elif data == "cp_rem_fsub":
            if not is_admin: return await query.answer("⚠️ Access Denied!", show_alert=True)
            await query.answer("➖ Removing Channel")
            try:
                ask = await client.ask(chat_id=user_id, text="<b>Send Channel ID to remove:</b>", timeout=60)
                cid = int(ask.text)
                await db.rem_channel(cid)
                await ask.reply(f"✅ Removed {cid}")
            except: pass

        # Premium Management Callbacks
        elif data.startswith("manage_prem_"):
            if not is_admin: return await query.answer("⚠️ Access Denied!", show_alert=True)
            await query.answer()
            uid = int(data.split("_")[-1])
            s1, e1 = get_random_button_style()
            s2, e2 = get_random_button_style()
            s3, e3 = get_random_button_style()
            buttons = [
                [InlineKeyboardButton("➕ Add Extra Days", callback_data=f"add_days_{uid}", icon_custom_emoji_id=e1, style=s1)],
                [InlineKeyboardButton("➖ Remove Premium", callback_data=f"rem_prem_{uid}", icon_custom_emoji_id=e2, style=s2)],
                [InlineKeyboardButton("🔙 Back", callback_data="back_to_list_prem", icon_custom_emoji_id=e3, style=s3)]
            ]
            await query.message.edit(f"<b>💎 Managing:</b> <code>{uid}</code>", reply_markup=InlineKeyboardMarkup(buttons))

        elif data.startswith("add_days_"):
            if not is_admin: return await query.answer("⚠️ Access Denied!", show_alert=True)
            await query.answer()
            uid = int(data.split("_")[-1])
            try:
                ask = await client.ask(chat_id=user_id, text=f"<b>Days to add for {uid}:</b>", timeout=60)
                await add_premium(uid, int(ask.text), 'd')
                await ask.reply(f"✅ Added {ask.text} days")
            except: pass

        elif data.startswith("rem_prem_"):
            if not is_admin: return await query.answer("⚠️ Access Denied!", show_alert=True)
            uid = int(data.split("_")[-1])
            await remove_premium(uid)
            await query.answer("✅ Removed", show_alert=True)
            # Fetch new list and update
            users = await get_all_premium_users()
            buttons = []
            for u in users:
                uid = u['user_id']
                rem = int(u['remaining_seconds'] // 86400)
                s, e = get_random_button_style()
                buttons.append([InlineKeyboardButton(f"👤 {uid} - {rem}d", callback_data=f"manage_prem_{uid}", icon_custom_emoji_id=e, style=s)])
            s, e = get_random_button_style()
            buttons.append([InlineKeyboardButton("• ᴄʟᴏsᴇ •", callback_data="close", icon_custom_emoji_id=e, style=s)])
            await query.message.edit("<b>💎 Premium Users List</b>", reply_markup=InlineKeyboardMarkup(buttons))

        elif data == "back_to_list_prem":
            if not is_admin: return await query.answer("⚠️ Access Denied!", show_alert=True)
            await query.answer()
            users = await get_all_premium_users()
            buttons = []
            for u in users:
                uid = u['user_id']
                rem = int(u['remaining_seconds'] // 86400)
                s, e = get_random_button_style()
                buttons.append([InlineKeyboardButton(f"👤 {uid} - {rem}d", callback_data=f"manage_prem_{uid}", icon_custom_emoji_id=e, style=s)])
            s, e = get_random_button_style()
            buttons.append([InlineKeyboardButton("• ᴄʟᴏsᴇ •", callback_data="close", icon_custom_emoji_id=e, style=s)])
            await query.message.edit("<b>💎 Premium Users List</b>", reply_markup=InlineKeyboardMarkup(buttons))

    except Exception as e:
        logging.error(f"Callback Error: {data} - {e}")
        try:
            await query.answer("⚠️ An error occurred! 🏯", show_alert=True)
        except: pass


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
