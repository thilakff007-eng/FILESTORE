#@ALONEKINGSTAR77_Botz
#@ALONEKINGSTAR77 on Tg

import asyncio
import motor.motor_asyncio
import time
import os
from config import DB_URI, DB_NAME
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)

default_verify = {
    'is_verified': False,
    'verified_time': 0,
    'verify_token': "",
    'link': ""
}

def new_user(id):
    return {
        '_id': id,
        'verify_status': {
            'is_verified': False,
            'verified_time': "",
            'verify_token': "",
            'link': ""
        }
    }

class Database:

    def __init__(self, DB_URI, DB_NAME):
        self.dbclient = motor.motor_asyncio.AsyncIOMotorClient(DB_URI)
        self.database = self.dbclient[DB_NAME]

        self.channel_data = self.database['channels']
        self.admins_data = self.database['admins']
        self.user_data = self.database['users']
        self.sex_data = self.database['sex']
        self.banned_user_data = self.database['banned_user']
        self.autho_user_data = self.database['autho_user']
        self.del_timer_data = self.database['del_timer']
        self.premium_data = self.database['premium_users']
        self.fsub_data = self.database['fsub']   
        self.rqst_fsub_data = self.database['request_forcesub']
        self.rqst_fsub_Channel_data = self.database['request_forcesub_channel']
        self.antibot_data = self.database['antibot_data']
        self.settings_data = self.database['settings']
        self.link_clicks_data = self.database['link_clicks']

        # Cache for del_timer
        self.del_timer_cache = None
        self.del_timer_cache_ts = 0

        # Cache for present users
        self.users_cache = set()

        # Cache for banned users
        self.banned_cache = {}
        self.banned_cache_time = 60

        # Cache for maintenance
        self.maintenance_cache = None
        self.maintenance_cache_ts = 0

        # Cache for shortener status
        self.shortener_cache = None
        self.shortener_cache_ts = 0

        # Cache for channel modes
        self.modes_cache = {}

        # Cache for show_channels
        self.channels_cache = None
        self.channels_cache_ts = 0
    async def present_user(self, user_id: int):
        if user_id in self.users_cache:
            return True
        found = await self.user_data.find_one({'_id': user_id})
        if found:
            self.users_cache.add(user_id)
        return bool(found)

    async def add_user(self, user_id: int):
        self.users_cache.add(user_id)
        await self.user_data.insert_one({'_id': user_id})
        return

    async def full_userbase(self):
        user_docs = await self.user_data.find().to_list(length=None)
        user_ids = [doc['_id'] for doc in user_docs]
        return user_ids

    async def count_users(self):
        return await self.user_data.count_documents({})

    async def del_user(self, user_id: int):
        await self.user_data.delete_one({'_id': user_id})
        return


    # ADMIN DATA
    async def admin_exist(self, admin_id: int):
        found = await self.admins_data.find_one({'_id': admin_id})
        return bool(found)

    async def add_admin(self, admin_id: int):
        if not await self.admin_exist(admin_id):
            await self.admins_data.insert_one({'_id': admin_id})
            return

    async def del_admin(self, admin_id: int):
        if await self.admin_exist(admin_id):
            await self.admins_data.delete_one({'_id': admin_id})
            return

    async def get_all_admins(self):
        users_docs = await self.admins_data.find().to_list(length=None)
        user_ids = [doc['_id'] for doc in users_docs]
        return user_ids

    async def count_admins(self):
        return await self.admins_data.count_documents({})


    # BAN USER DATA
    async def ban_user_exist(self, user_id: int):
        now = time.time()
        if user_id in self.banned_cache:
            val, ts = self.banned_cache[user_id]
            if now - ts < self.banned_cache_time:
                return val

        found = await self.banned_user_data.find_one({'_id': user_id})
        res = bool(found)
        self.banned_cache[user_id] = (res, now)
        return res

    async def add_ban_user(self, user_id: int):
        self.banned_cache[user_id] = (True, time.time())
        if not await self.ban_user_exist(user_id):
            await self.banned_user_data.insert_one({'_id': user_id})
            return

    async def del_ban_user(self, user_id: int):
        if await self.ban_user_exist(user_id):
            await self.banned_user_data.delete_one({'_id': user_id})
            return

    async def get_ban_users(self):
        users_docs = await self.banned_user_data.find().to_list(length=None)
        user_ids = [doc['_id'] for doc in users_docs]
        return user_ids



    # AUTO DELETE TIMER SETTINGS
    async def set_del_timer(self, value: int):
        self.del_timer_cache = value
        self.del_timer_cache_ts = time.time()
        existing = await self.del_timer_data.find_one({})
        if existing:
            await self.del_timer_data.update_one({}, {'$set': {'value': value}})
        else:
            await self.del_timer_data.insert_one({'value': value})

    async def get_del_timer(self):
        now = time.time()
        if self.del_timer_cache is not None and now - self.del_timer_cache_ts < 300: # 5 min cache
            return self.del_timer_cache

        data = await self.del_timer_data.find_one({})
        res = 0
        if data:
            res = data.get('value', 600)

        self.del_timer_cache = res
        self.del_timer_cache_ts = now
        return res


    # CHANNEL MANAGEMENT
    async def channel_exist(self, channel_id: int):
        found = await self.fsub_data.find_one({'_id': channel_id})
        return bool(found)

    async def add_channel(self, channel_id: int):
        if not await self.channel_exist(channel_id):
            await self.fsub_data.insert_one({'_id': channel_id})
            return

    async def rem_channel(self, channel_id: int):
        if await self.channel_exist(channel_id):
            await self.fsub_data.delete_one({'_id': channel_id})
            return

    async def del_channel(self, channel_id: int):
        return await self.rem_channel(channel_id)

    async def show_channels(self):
        now = time.time()
        if self.channels_cache is not None and now - self.channels_cache_ts < 60:
            return self.channels_cache

        channel_docs = await self.fsub_data.find().to_list(length=None)
        channel_ids = [doc['_id'] for doc in channel_docs]
        self.channels_cache = channel_ids
        self.channels_cache_ts = now
        return channel_ids

    
# Get current mode of a channel
    async def get_channel_mode(self, channel_id: int):
        now = time.time()
        if channel_id in self.modes_cache:
            val, ts = self.modes_cache[channel_id]
            if now - ts < 60:
                return val

        data = await self.fsub_data.find_one({'_id': channel_id})
        res = data.get("mode", "off") if data else "off"
        self.modes_cache[channel_id] = (res, now)
        return res

    # Set mode of a channel
    async def set_channel_mode(self, channel_id: int, mode: str):
        self.modes_cache[channel_id] = (mode, time.time())
        await self.fsub_data.update_one(
            {'_id': channel_id},
            {'$set': {'mode': mode}},
            upsert=True
        )

    # REQUEST FORCE-SUB MANAGEMENT

    # Add the user to the set of users for a   specific channel
    async def req_user(self, channel_id: int, user_id: int):
        try:
            await self.rqst_fsub_Channel_data.update_one(
                {'_id': int(channel_id)},
                {'$addToSet': {'user_ids': int(user_id)}},
                upsert=True
            )
        except Exception as e:
            print(f"[DB ERROR] Failed to add user to request list: {e}")


    # Method 2: Remove a user from the channel set
    async def del_req_user(self, channel_id: int, user_id: int):
        # Remove the user from the set of users for the channel
        await self.rqst_fsub_Channel_data.update_one(
            {'_id': channel_id}, 
            {'$pull': {'user_ids': user_id}}
        )

    # Check if the user exists in the set of the channel's users
    async def req_user_exist(self, channel_id: int, user_id: int):
        try:
            found = await self.rqst_fsub_Channel_data.find_one({
                '_id': int(channel_id),
                'user_ids': int(user_id)
            })
            return bool(found)
        except Exception as e:
            print(f"[DB ERROR] Failed to check request list: {e}")
            return False  


    # Method to check if a channel exists using show_channels
    async def reqChannel_exist(self, channel_id: int):
    # Get the list of all channel IDs from the database
        channel_ids = await self.show_channels()
        #print(f"All channel IDs in the database: {channel_ids}")

    # Check if the given channel_id is in the list of channel IDs
        if channel_id in channel_ids:
            #print(f"Channel {channel_id} found in the database.")
            return True
        else:
            #print(f"Channel {channel_id} NOT found in the database.")
            return False



    # VERIFICATION MANAGEMENT
    async def db_verify_status(self, user_id):
        user = await self.user_data.find_one({'_id': user_id})
        if user:
            return user.get('verify_status', default_verify)
        return default_verify

    async def db_update_verify_status(self, user_id, verify):
        await self.user_data.update_one({'_id': user_id}, {'$set': {'verify_status': verify}})

    async def get_verify_status(self, user_id):
        verify = await self.db_verify_status(user_id)
        return verify

    async def update_verify_status(self, user_id, verify_token="", is_verified=False, verified_time=0, link=""):
        current = await self.db_verify_status(user_id)
        current['verify_token'] = verify_token
        current['is_verified'] = is_verified
        current['verified_time'] = verified_time
        current['link'] = link
        await self.db_update_verify_status(user_id, current)

    # Set verify count (overwrite with new value)
    async def set_verify_count(self, user_id: int, count: int):
        await self.sex_data.update_one({'_id': user_id}, {'$set': {'verify_count': count}}, upsert=True)

    # Get verify count (default to 0 if not found)
    async def get_verify_count(self, user_id: int):
        user = await self.sex_data.find_one({'_id': user_id})
        if user:
            return user.get('verify_count', 0)
        return 0

    # Reset all users' verify counts to 0
    async def reset_all_verify_counts(self):
        await self.sex_data.update_many(
            {},
            {'$set': {'verify_count': 0}} 
        )

    # Get total verify count across all users
    async def get_total_verify_count(self):
        pipeline = [
            {"$group": {"_id": None, "total": {"$sum": "$verify_count"}}}
        ]
        result = await self.sex_data.aggregate(pipeline).to_list(length=1)
        return result[0]["total"] if result else 0

    # MAINTENANCE MODE
    async def set_maintenance(self, expiry_time: datetime):
        self.maintenance_cache = expiry_time
        self.maintenance_cache_ts = time.time()
        await self.settings_data.update_one(
            {'_id': 'maintenance'},
            {'$set': {'expiry': expiry_time}},
            upsert=True
        )

    async def get_maintenance(self):
        now = time.time()
        if self.maintenance_cache_ts > 0 and now - self.maintenance_cache_ts < 60:
            return self.maintenance_cache

        data = await self.settings_data.find_one({'_id': 'maintenance'})
        res = data.get('expiry') if data else None
        self.maintenance_cache = res
        self.maintenance_cache_ts = now
        return res

    # SHORTENER SETTINGS
    async def set_shortener_status(self, status: bool):
        self.shortener_cache = status
        self.shortener_cache_ts = time.time()
        await self.settings_data.update_one(
            {'_id': 'shortener'},
            {'$set': {'enabled': status}},
            upsert=True
        )

    async def get_shortener_status(self):
        now = time.time()
        if self.shortener_cache is not None and now - self.shortener_cache_ts < 60:
            return self.shortener_cache

        data = await self.settings_data.find_one({'_id': 'shortener'})
        res = data.get('enabled', True) if data else True
        self.shortener_cache = res
        self.shortener_cache_ts = now
        return res

    async def set_setting(self, key: str, value):
        await self.settings_data.update_one(
            {'_id': key},
            {'$set': {'value': value}},
            upsert=True
        )

    async def get_setting(self, key: str, default=None):
        data = await self.settings_data.find_one({'_id': key})
        return data.get('value', default) if data else default

    async def get_protect_content(self):
        return await self.get_setting("protect_content", False)

    async def set_protect_content(self, status: bool):
        await self.set_setting("protect_content", status)

    # ANTI-BOT DATA
    async def get_antibot_data(self, user_id: int):
        user = await self.user_data.find_one({'_id': user_id})
        if user:
            return user.get('antibot', {})
        return {}

    async def update_antibot_data(self, user_id: int, data: dict):
        await self.user_data.update_one({'_id': user_id}, {'$set': {'antibot': data}}, upsert=True)

    # TOKEN VERIFICATION
    async def add_verify_token(self, token: str, user_id: int, payload: str):
        # Ensure TTL index exists for automatic expiration after 1 hour
        try:
            await self.antibot_data.create_index("created_at", expireAfterSeconds=3600)
        except Exception as e:
            logging.debug(f"Index creation skipped or failed: {e}")

        await self.antibot_data.insert_one({
            'token': token,
            'user_id': user_id,
            'payload': payload,
            'status': 'start',
            'created_at': datetime.utcnow()
        })

    async def get_verify_token(self, token: str):
        return await self.antibot_data.find_one({'token': token})

    async def update_token_status(self, token: str, status: str, extra_data: dict = None):
        update_doc = {'$set': {'status': status}}
        if extra_data:
            update_doc['$set'].update(extra_data)
        await self.antibot_data.update_one({'token': token}, update_doc)

    async def delete_verify_token(self, token: str):
        await self.antibot_data.delete_one({'token': token})

    # PREMIUM MANAGEMENT
    async def get_premium_user(self, user_id: int):
        data = await self.premium_data.find_one({'_id': user_id})
        if data:
            # Check if expired
            expiry = data.get('expiry')
            if expiry and datetime.utcnow() > expiry:
                await self.remove_premium_user(user_id)
                return None
            return data
        return None

    async def add_premium_user(self, user_id: int, expiry: datetime):
        await self.premium_data.update_one(
            {'_id': user_id},
            {'$set': {'expiry': expiry}},
            upsert=True
        )

    async def remove_premium_user(self, user_id: int):
        await self.premium_data.delete_one({'_id': user_id})

    async def get_all_premium_users(self):
        # Cleanup expired before returning
        await self.premium_data.delete_many({'expiry': {'$lt': datetime.utcnow()}})
        return await self.premium_data.find().to_list(length=None)

    # LINK CLICK TRACKING
    async def track_link_click(self, link_id: str):
        await self.link_clicks_data.update_one(
            {'_id': link_id},
            {
                '$inc': {'total_clicks': 1, 'daily_clicks': 1},
                '$set': {'last_click': datetime.utcnow()}
            },
            upsert=True
        )

    async def get_top_links_daily(self, limit=10):
        return await self.link_clicks_data.find().sort('daily_clicks', -1).limit(limit).to_list(length=limit)

    async def reset_daily_link_clicks(self):
        await self.link_clicks_data.update_many({}, {'$set': {'daily_clicks': 0}})


db = Database(DB_URI, DB_NAME)
