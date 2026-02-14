#(©)⚡𝗛𝗘𝗠𝗔𝗡𝗧𝗛⚡
#@ALONEKINGSTAR77





from aiohttp import web
from .route import routes


async def web_server(bot):
    web_app = web.Application(client_max_size=30000000)
    web_app['bot'] = bot
    web_app.add_routes(routes)
    return web_app
