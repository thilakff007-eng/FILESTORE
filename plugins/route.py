from aiohttp import web
import random
from config import BOT_NAME, PICS, MAIN_LINK, OWNER_ID

routes = web.RouteTableDef()

def get_random_pic():
    return random.choice(PICS)

WATERMARK_STYLE = """
            .watermark {
                position: fixed;
                bottom: 10px;
                left: 10px;
                font-size: 18px;
                font-weight: bold;
                z-index: 999;
                opacity: 0.8;
                background: linear-gradient(to right, #ff0000, #ff7f00, #ffff00, #00ff00, #0000ff, #4b0082, #8f00ff);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                animation: rainbow_animation 3s linear infinite;
                background-size: 200% auto;
                pointer-events: none;
                text-shadow: 0 0 5px rgba(0,0,0,0.5);
            }
            @keyframes rainbow_animation {
                0% { background-position: 0% 50%; }
                100% { background-position: 200% 50%; }
            }
"""

WATERMARK_DIV = '<div class="watermark">OTAKUSTARTELUGU</div>'

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    anime_pic = get_random_pic()
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
                background: #1a1a2e;
                color: white;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                text-align: center;
                overflow: hidden;
            }}
            .background {{
                position: fixed;
                top: 0; left: 0; width: 100%; height: 100%;
                background: linear-gradient(rgba(26, 26, 46, 0.8), rgba(26, 26, 46, 0.8)), url('{anime_pic}') no-repeat center center;
                background-size: cover;
                z-index: -1;
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
            .logo {{
                width: 120px;
                height: 120px;
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
            {WATERMARK_STYLE}
        </style>
    </head>
    <body>
        <div class="background"></div>
        {WATERMARK_DIV}
        <div class="container">
            <img src="{anime_pic}" alt="Logo" class="logo">
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

@routes.get(f"/link/__{OWNER_ID}__" + "/{id}")
async def redirect_handler(request):
    file_id = request.match_info.get('id')
    from helper_func import get_shortlink
    from config import URL, SHORTLINK_URL, SHORTLINK_API

    bridge_link = f"{URL}/get/{file_id}"
    try:
        short_link = await get_shortlink(SHORTLINK_URL, SHORTLINK_API, bridge_link)
        # Direct redirect for maximum reliability and speed
        return web.HTTPFound(location=short_link)
    except Exception as e:
        print(f"Error in redirector: {e}")
        return web.HTTPFound(location=bridge_link)

@routes.get("/get/{id}")
async def get_route_handler(request):
    bot = request.app['bot']
    file_id = request.match_info.get('id')
    from config import BOT_NAME, PICS
    anime_pic = random.choice(PICS)

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Verification - {BOT_NAME}</title>
        <style>
            body {{
                margin: 0;
                padding: 0;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: #1a1a2e;
                color: white;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                text-align: center;
            }}
            .background {{
                position: fixed;
                top: 0; left: 0; width: 100%; height: 100%;
                background: linear-gradient(rgba(26, 26, 46, 0.8), rgba(26, 26, 46, 0.8)), url('{anime_pic}') no-repeat center center;
                background-size: cover;
                z-index: -1;
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
            .logo {{
                width: 100px;
                height: 100px;
                border-radius: 50%;
                margin-bottom: 20px;
                border: 4px solid #e94560;
                object-fit: cover;
            }}
            h2 {{
                color: #e94560;
                margin-bottom: 10px;
            }}
            .status {{
                font-size: 1.1em;
                margin-bottom: 20px;
                color: #00d2ff;
            }}
            .btn {{
                display: none;
                padding: 15px 40px;
                background-color: #e94560;
                color: white;
                text-decoration: none;
                border-radius: 30px;
                font-weight: bold;
                transition: transform 0.3s ease, background-color 0.3s ease;
                border: none;
                cursor: pointer;
                font-size: 1em;
            }}
            .btn:hover {{
                background-color: #ff4d6d;
                transform: scale(1.05);
            }}
            #timer {{
                font-weight: bold;
                color: #e94560;
            }}
            footer {{
                margin-top: 30px;
                font-size: 0.9em;
                opacity: 0.5;
            }}
            {WATERMARK_STYLE}
        </style>
    </head>
    <body>
        <div class="background"></div>
        {WATERMARK_DIV}
        <div class="container">
            <img src="{anime_pic}" alt="Logo" class="logo">
            <h2>Verify You're Human</h2>
            <p class="status" id="status_text">Please wait <span id="timer">5</span> seconds...</p>
            <a href="https://t.me/{bot.username}?start={file_id}" class="btn" id="verify_btn">Verify & Open Telegram</a>
        </div>
        <script>
            let timeLeft = 5;
            const timerElement = document.getElementById('timer');
            const btnElement = document.getElementById('verify_btn');
            const statusText = document.getElementById('status_text');

            const countdown = setInterval(() => {{
                timeLeft--;
                timerElement.innerText = timeLeft;
                if (timeLeft <= 0) {{
                    clearInterval(countdown);
                    statusText.innerText = "Verification Ready!";
                    timerElement.style.display = 'none';
                    btnElement.style.display = 'inline-block';

                    setTimeout(() => {{
                        window.location.href = "tg://resolve?domain={bot.username}&start={file_id}";
                    }}, 500);
                }}
            }}, 1000);
        </script>
        <footer>
            &copy; 2025 {BOT_NAME} | Secure Verification
        </footer>
    </body>
    </html>
    """
    return web.Response(text=html_content, content_type='text/html')
