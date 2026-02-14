from aiohttp import web
import random
from config import BOT_NAME, PICS, MAIN_LINK

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    anime_pic = random.choice(PICS)
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{BOT_NAME} - File Store</title>
        <style>
            body {{
                margin: 0;
                padding: 0;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                color: white;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                text-align: center;
            }}
            .container {{
                background: rgba(255, 255, 255, 0.05);
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                max-width: 500px;
                width: 90%;
            }}
            img {{
                width: 150px;
                height: 150px;
                border-radius: 50%;
                margin-bottom: 20px;
                border: 4px solid #e94560;
                object-fit: cover;
            }}
            h1 {{
                margin: 10px 0;
                font-size: 2.5em;
                color: #e94560;
            }}
            p {{
                font-size: 1.1em;
                opacity: 0.8;
                margin-bottom: 30px;
            }}
            .btn {{
                display: inline-block;
                padding: 12px 30px;
                background-color: #e94560;
                color: white;
                text-decoration: none;
                border-radius: 30px;
                font-weight: bold;
                transition: transform 0.3s ease, background-color 0.3s ease;
            }}
            .btn:hover {{
                background-color: #ff4d6d;
                transform: scale(1.05);
            }}
            footer {{
                margin-top: 30px;
                font-size: 0.9em;
                opacity: 0.5;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <img src="{anime_pic}" alt="Bot Logo">
            <h1>{BOT_NAME}</h1>
            <p>Welcome to the official File Store Bot. Store and retrieve your files securely and at maximum speed.</p>
            <a href="{MAIN_LINK}" class="btn">Join Our Community</a>
        </div>
        <footer>
            &copy; 2025 {BOT_NAME} | Powered by Render
        </footer>
    </body>
    </html>
    """
    return web.Response(text=html_content, content_type='text/html')

@routes.get("/get/{id}")
async def get_route_handler(request):
    file_id = request.match_info.get('id')
    from config import BOT_NAME, BOT_USERNAME
    # Redirect to the bot with the start parameter
    # We use a simple HTML redirect to ensure it works well with mobile browsers
    html_redirect = f"""
    <html>
    <head>
        <title>Redirecting...</title>
        <meta http-equiv="refresh" content="0; url=https://t.me/{BOT_USERNAME}?start={file_id}">
    </head>
    <body>
        <p>Redirecting to Telegram... if not redirected <a href="https://t.me/{BOT_USERNAME}?start={file_id}">click here</a>.</p>
        <script>window.location.href = "https://t.me/{BOT_USERNAME}?start={file_id}";</script>
    </body>
    </html>
    """
    return web.Response(text=html_redirect, content_type='text/html')
