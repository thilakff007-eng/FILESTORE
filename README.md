# ⚡𝗛𝗘𝗠𝗔𝗡𝗧𝗛⚡ File Store Bot

An advanced, high-performance Telegram File Store Bot with a secure, multi-stage verification flow and Anime-themed UI.

## 🏯 Features
- **Unlimited Force Subscribe (FSUB):** Support for multiple channels/groups.
- **Advanced Verification Flow:**
  - **Step 1:** Frontend Human Check (Task Page).
  - **Step 2:** Premium Shortlink (Shrinkearn).
  - **Step 3:** Secure "Hold to Verify" (5-second interaction).
- **Branding:** Fully rebranded as ⚡𝗛𝗘𝗠𝗔𝗡𝗧𝗛⚡ (@ALONEKINGSTAR77).
- **Performance:** Async handlers, non-blocking DB operations, and optimized caching.
- **UI:** Modern Anime-themed web UI with neon effects and loading animations.
- **Auto-Delete:** Files automatically delete after a set time to ensure privacy.
- **Admin Panel:** Comprehensive controls for FSUB, maintenance, and user management.

## 🚀 Deployment (Render/Docker)
1. **Fork the Repository:** Clone this repo to your Github account.
2. **Create Web Service on Render:**
   - Connect your Github repo.
   - Choose **Docker** as the Runtime.
   - Add the required environment variables (see below).
   - Use the `worker` start command or let Dockerfile handle it.

## ⚙️ Environment Variables
| Variable | Description |
|----------|-------------|
| `TG_BOT_TOKEN` | Your Telegram Bot Token (@BotFather) |
| `API_ID` | Your Telegram API ID |
| `API_HASH` | Your Telegram API HASH |
| `DATABASE_URL` | MongoDB Connection URI |
| `DATABASE_NAME` | MongoDB Database Name (e.g., Cluster0) |
| `OWNER_ID` | Your Telegram User ID |
| `CHANNEL_ID` | Database Channel ID (Bot must be Admin) |
| `SHORTLINK_URL` | Shortener domain (e.g., shrinkearn.com) |
| `SHORTLINK_API` | Shortener API Key |
| `URL` | Your App's public URL (without https://) |

## 🛠️ Admin Commands
- `/start` - Check bot status.
- `/broadcast` - Send message to all users.
- `/addfsub` - Add a Force Subscribe channel.
- `/removefsub` - Remove a channel from FSUB.
- `/fsublist` - List all FSUB channels.
- `/maintenance` - Toggle maintenance mode.
- `/stats` - View bot and user statistics.
- `/addpremium` - Grant premium status to a user.

## 🌸 Credits
- **Bot Name:** ⚡𝗛𝗘𝗠𝗔𝗡𝗧𝗛⚡
- **Username:** [@ALONEKINGSTAR77](https://t.me/ALONEKINGSTAR77)
- **Community:** [Otaku Star Telugu](https://t.me/otakustartelugu)

---
*Built with ❤️ for the community.*
