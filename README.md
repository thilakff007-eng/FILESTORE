<h1 align="center">
    ⚡ ʜᴇᴍᴀɴᴛʜ ғɪʟᴇ sᴛᴏʀᴇ ⚡
</h1>

<p align="center">
  <img src="https://iili.io/q94kIvp.png" alt="Banner">
</p>

<p align="center">
  <a href="https://t.me/otakustartelugu">
    <img src="https://img.shields.io/badge/Telegram-Community-blue?style=for-the-badge&logo=telegram" alt="Telegram">
  </a>
  <a href="https://t.me/ALONEKINGSTAR77">
    <img src="https://img.shields.io/badge/Developer-ALONEKINGSTAR77-red?style=for-the-badge&logo=telegram" alt="Developer">
  </a>
</p>

---

## 🏯 Features

- ⚡ **Unlimited Force Subscribe:** Support for unlimited channels/groups with auto-verification.
- 💎 **Premium System:** Grant premium access to users with customizable durations.
- 🏯 **Anime Theme UI:** Beautifully designed interface with random anime wallpapers.
- 🚀 **High Performance:** Optimized with async handlers and non-blocking database operations.
- 🛡️ **Admin Tools:** Comprehensive tools for broadcasting, banning, and managing FSUB.
- 🗑️ **Auto File Delete:** Automatically delete shared files after a set duration.
- 🐳 **Docker Ready:** Easy deployment using Docker and optimized for Render.

## 🚀 Deployment

### 1. Deploy on Render (Recommended)

1. Fork this repository.
2. Create a new Web Service on [Render](https://render.com).
3. Connect your fork.
4. Set the environment variables as listed below.
5. Use the following settings:
   - **Runtime:** Docker
   - **Plan:** Free or better

### 2. Manual Deployment (VPS)

```bash
git clone https://github.com/ALONEKINGSTAR77-Bots/FileStore
cd FileStore
pip3 install -r requirements.txt
# Edit config.py or set environment variables
python3 main.py
```

## ⚙️ Environment Variables

| Variable | Description |
| --- | --- |
| `API_ID` | Your Telegram API ID |
| `API_HASH` | Your Telegram API Hash |
| `TG_BOT_TOKEN` | Your Bot Token from @BotFather |
| `OWNER_ID` | Your Telegram User ID |
| `DATABASE_URL` | Your MongoDB Connection URL |
| `DATABASE_NAME` | Your MongoDB Database Name |

## 🛠️ Admin Commands

- `/start` - Start the bot.
- `/broadcast` - Broadcast a message to all users.
- `/stats` - View bot statistics.
- `/addfsub` - Add a Force Subscribe channel.
- `/removefsub` - Remove a Force Subscribe channel.
- `/fsublist` - List all Force Subscribe channels.
- `/ban` - Ban a user.
- `/unban` - Unban a user.

---

<p align="center">
    <b>⚡ Created with ❤️ by <a href="https://t.me/otakustartelugu">⚡𝗛𝗘𝗠𝗔𝗡𝗧𝗛⚡</a></b>
</p>
