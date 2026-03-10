# ⚡𝗛𝗘𝗠𝗔𝗡𝗧𝗛⚡ File Store Bot

An advanced, high-performance Telegram File Store Bot with a secure, multi-stage verification flow and Anime-themed UI.

## 🏯 Features
- **Unlimited Force Subscribe (FSUB):** Support for multiple channels/groups with interactive management.
- **Request Mode FSUB:** Automatically handles and verifies join requests for private channels.
- **Advanced Verification Flow:**
  - **Step 1:** Frontend Human Check (Anime Task Page).
  - **Step 2:** Premium Shortlink (mdiskshort.in/).
  - **Step 3:** Secure "Hold to Verify" (5-second interaction to prevent automated scripts).
- **Premium Management System:** Interactive UI for adding/listing/managing premium users with expiry tracking.
- **Branding:** Fully rebranded as ⚡𝗛𝗘𝗠𝗔𝗡𝗧𝗛⚡ (@ALONEKINGSTAR77).
- **Performance:** Async handlers, non-blocking DB operations, and optimized caching with batch broadcasting.
- **UI:** Modern Anime-themed web UI with neon effects, loading animations, and fast callback responses.
- **Auto-Delete:** Files automatically delete after a set time to ensure privacy.
- **Maintenance Mode:** Admin can toggle maintenance to perform updates safely.

## 🚀 Commands
### User Commands
- `/start` - Start the bot and get files.
- `/help` - View help information.
- `/about` - About the bot.
- `/myplan` - Check your premium status.

### Admin Commands
- `/control_panel` - Real-time settings management.
- `/batch` - Create batch links for multiple files.
- `/genlink` - Generate a single file link.
- `/custom_batch` - Create custom batches by copying messages.
- `/broadcast` - Broadcast message to all users.
- `/dbroadcast` - Broadcast with auto-delete timer.
- `/pbroadcast` - Pin broadcasted messages.
- `/addfsub` - Add a Force Subscribe channel.
- `/removefsub` - Remove a Force Subscribe channel.
- `/fsublist` - List all FSUB channels.
- `/fsub_mode` - Toggle Request Mode for FSUB.
- `/add_admin` - Add a new bot admin.
- `/deladmin` - Remove an admin.
- `/admins` - List all bot admins.
- `/addpremium` - Add a premium user.
- `/remove_premium` - Revoke premium access.
- `/premium_users` - List all premium users.
- `/stats` - View detailed bot statistics.
- `/count` - Check verification counts.
- `/maintenance` - Toggle maintenance mode.
- `/hash` - Manage link masking algorithms.
- `/delreq` - Cleanup leftover FSUB join requests.

## ⚙️ Environment Variables
| Variable | Description |
|----------|-------------|
| `TG_BOT_TOKEN` | Your Telegram Bot Token (@BotFather) |
| `APP_ID` | Your Telegram API ID |
| `API_HASH` | Your Telegram API HASH |
| `DATABASE_URL` | MongoDB Connection URI |
| `DATABASE_NAME` | MongoDB Database Name (e.g., Cluster0) |
| `OWNER_ID` | Your Telegram User ID (Owner) |
| `CHANNEL_ID` | Database Channel ID (Bot must be Admin) |
| `SHORTLINK_URL` | Shortener domain (e.g., mdiskshort.in/) |
| `SHORTLINK_API` | Shortener API Key |
| `URL` | Your App's public URL (without https://) (e.g., filesanimes.onrender.com) |
| `TUTORIAL` | Tutorial video link for users. |

## 🌸 Credits
- **Bot Name:** ⚡𝗛𝗘𝗠𝗔𝗡𝗧𝗛⚡
- **Username:** [@ALONEKINGSTAR77](https://t.me/ALONEKINGSTAR77)
- **Main Link:** [otakustartelugu](https://t.me/otakustartelugu)

---
*Built with ❤️ for the community by @ALONEKINGSTAR77.*
