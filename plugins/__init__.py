#(©)⚡𝗛𝗘𝗠𝗔𝗡𝗧𝗛⚡
#@ALONEKINGSTAR77





from aiohttp import web
import aiohttp
from .route import routes


async def web_server(bot):
    web_app = web.Application(client_max_size=30000000)
    web_app['bot'] = bot

    async def on_startup(app):
        app['http_session'] = aiohttp.ClientSession()

    async def on_cleanup(app):
        await app['http_session'].close()

    web_app.on_startup.append(on_startup)
    web_app.on_cleanup.append(on_cleanup)
    web_app.add_routes(routes)
    return web_app
