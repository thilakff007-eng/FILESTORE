# ⚡𝗛𝗘𝗠𝗔𝗡𝗧𝗛⚡ File Store Bot

An advanced, high-performance Telegram File Store Bot with a secure, multi-stage verification flow and Anime-themed UI.

## 🏯 Features
- **Unlimited Force Subscribe (FSUB):** Support for multiple channels/groups with interactive management.
- **Request Mode FSUB:** Automatically handles and verifies join requests for private channels.
- **Advanced Verification Flow:**
  - **Step 1:** Frontend Human Check (Anime Task Page).
  - **Step 2:** Premium Shortlink (arolinks.com).
  - **Step 3:** Secure "Hold to Verify" (5-second interaction to prevent automated scripts).
- **Premium Management System:** Interactive UI for adding/listing/managing premium users with expiry tracking.
- **Branding:** Fully rebranded as ⚡𝗛𝗘𝗠𝗔𝗡𝗧𝗛⚡ (@ALONEKINGSTAR77).
- **Performance:** Async handlers, non-blocking DB operations, and optimized caching with batch broadcasting.
- **UI:** Modern Anime-themed web UI with neon effects, loading animations, and fast callback responses.
- **Auto-Delete:** Files automatically delete after a set time to ensure privacy.
- **Maintenance Mode:** Admin can toggle maintenance to perform updates safely.

## 🚀 Deployment (Render/Docker)
1. **Fork the Repository:** Clone this repo to your Github account.
2. **Create Web Service on Render:**
   - Connect your Github repo.
   - Choose **Docker** as the Runtime.
   - Add the required environment variables (see below).
   - Render will automatically build the image using the provided `Dockerfile`.

## ⚙️ Environment Variables
| Variable | Description |
|----------|-------------|
| `TG_BOT_TOKEN` | Your Telegram Bot Token (@BotFather) |
| `API_ID` | Your Telegram API ID |
| `API_HASH` | Your Telegram API HASH |
| `DATABASE_URL` | MongoDB Connection URI |
| `DATABASE_NAME` | MongoDB Database Name (e.g., Cluster0) |
| `OWNER_ID` | Your Telegram User ID (Owner) |
| `CHANNEL_ID` | Database Channel ID (Bot must be Admin) |
| `SHORTLINK_URL` | Shortener domain (e.g., arolinks.com) |
| `SHORTLINK_API` | Shortener API Key |
| `URL` | Your App's public URL (without https://) |
| `TUTORIAL` | Tutorial video link for users. |

## 🛠️ Admin Commands
- `/start` - Check bot status and uptime.
- `/broadcast` - Broadcast message to all users (Async).
- `/pbroadcast` - Broadcast and Pin message.
- `/dbroadcast` - Broadcast with auto-delete timer.
- `/addfsub` - Add a Force Subscribe channel.
- `/removefsub` - Remove a channel from FSUB.
- `/fsublist` - List all FSUB channels.
- `/maintenance` - Toggle maintenance mode (e.g., `/maintenance 1h` or `/maintenance off`).
- `/stats` - View bot and user statistics.
- `/addpremium` - Interactive flow to add premium users.
- `/listpremium` - Interactive list to manage premium users.
- `/admins` - List current bot admins.
- `/add_admin` - Add a new bot admin (Owner only).
- `/deladmin` - Remove a bot admin (Owner only).

## 🌸 Credits
- **Bot Name:** ⚡𝗛𝗘𝗠𝗔𝗡𝗧𝗛⚡
- **Username:** [@ALONEKINGSTAR77](https://t.me/ALONEKINGSTAR77)
- **Main Link:** [otakustartelugu](https://t.me/otakustartelugu)

---
*Built with ❤️ for the community.*
