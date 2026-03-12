import asyncio
from unittest.mock import MagicMock
import sys
import os

# Mock the database and config to avoid actual connections
sys.modules['database.database'] = MagicMock()
sys.modules['config'] = MagicMock()

import config
config.BOT_NAME = "TEST_BOT"
config.PICS = ["pic1"]
config.MAIN_LINK = "http://link"
config.URL = "http://url"
config.RECAPTCHA_SITE_KEY = "site_key"
config.RECAPTCHA_SECRET_KEY = "secret_key"
config.BOT_USERNAME = "bot_username"

from plugins.route import root_route_handler

class MockRequest:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'}
    app = {}
    remote = "127.0.0.1"

async def test():
    try:
        req = MockRequest()
        resp = await root_route_handler(req)
        print("Root Handler Success")
    except Exception as e:
        import traceback
        print("Root Handler Failed:")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test())
