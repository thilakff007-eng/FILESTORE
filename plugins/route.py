from aiohttp import web
import random
from config import BOT_NAME, PICS, MAIN_LINK, OWNER_ID

routes = web.RouteTableDef()

def get_random_pic():
    return random.choice(PICS)

WATERMARK_STYLE = """
            .watermark {
                position: fixed;
                bottom: 15px;
                left: 15px;
                font-size: 22px;
                font-weight: 900;
                z-index: 999;
                opacity: 0.9;
                background: linear-gradient(45deg, #ff0000, #ff7f00, #ffff00, #00ff00, #0000ff, #4b0082, #8f00ff);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                animation: rainbow_animation 2s linear infinite;
                background-size: 400% 400%;
                pointer-events: none;
                text-shadow: 0 0 10px rgba(255,255,255,0.3);
                font-family: 'Arial Black', sans-serif;
                letter-spacing: 2px;
            }
            @keyframes rainbow_animation {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
"""

WATERMARK_DIV = '<div class="watermark">⚡ OTAKUSTARTELUGU ⚡</div>'

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    anime_pic = get_random_pic()
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{BOT_NAME} - Advanced File Store</title>
        <style>
            body {{
                margin: 0;
                padding: 0;
                font-family: 'Poppins', sans-serif;
                background: radial-gradient(circle, #1a1a2e, #16213e, #0f3460);
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
                background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), url('{anime_pic}') no-repeat center center;
                background-size: cover;
                z-index: -1;
                filter: blur(8px);
                transform: scale(1.1);
            }}
            .container {{
                background: rgba(255, 255, 255, 0.05);
                padding: 50px;
                border-radius: 30px;
                box-shadow: 0 0 30px rgba(233, 69, 96, 0.4), 0 0 60px rgba(233, 69, 96, 0.1);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                max-width: 550px;
                width: 90%;
                animation: float 6s ease-in-out infinite;
            }}
            @keyframes float {{
                0% {{ transform: translateY(0px); box-shadow: 0 0 30px rgba(233, 69, 96, 0.4); }}
                50% {{ transform: translateY(-20px); box-shadow: 0 0 50px rgba(233, 69, 96, 0.6); }}
                100% {{ transform: translateY(0px); box-shadow: 0 0 30px rgba(233, 69, 96, 0.4); }}
            }}
            .logo {{
                width: 140px;
                height: 140px;
                border-radius: 50%;
                margin-bottom: 25px;
                border: 4px solid #e94560;
                object-fit: cover;
                box-shadow: 0 0 20px #e94560;
                transition: transform 0.5s;
            }}
            .logo:hover {{
                transform: rotate(360deg) scale(1.1);
            }}
            h1 {{
                margin: 10px 0;
                font-size: 3em;
                color: #fff;
                text-shadow: 0 0 10px #e94560, 0 0 20px #e94560, 0 0 30px #e94560;
                font-weight: 800;
            }}
            p {{
                font-size: 1.2em;
                opacity: 0.9;
                margin-bottom: 35px;
                color: #e0e0e0;
                line-height: 1.6;
            }}
            .btn {{
                display: inline-block;
                padding: 15px 40px;
                background: linear-gradient(45deg, #e94560, #ff4d6d);
                color: white;
                text-decoration: none;
                border-radius: 50px;
                font-weight: 700;
                transition: all 0.4s ease;
                box-shadow: 0 0 20px rgba(233, 69, 96, 0.6);
                text-transform: uppercase;
                letter-spacing: 2px;
            }}
            .btn:hover {{
                background: linear-gradient(45deg, #ff4d6d, #e94560);
                transform: scale(1.15);
                box-shadow: 0 0 40px #e94560;
                letter-spacing: 4px;
            }}
            footer {{
                margin-top: 40px;
                font-size: 1em;
                opacity: 0.8;
                color: #e94560;
                font-weight: bold;
                text-shadow: 0 0 5px rgba(0,0,0,0.5);
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
            <p>Experience the future of file storage. Secure, encrypted, and lightning fast. Your files are safe with us.</p>
            <a href="{MAIN_LINK}" class="btn">🚀 Join Community</a>
        </div>
        <footer>
            &copy; 2025 {BOT_NAME} | Premium Experience
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

    base_url = f"https://{URL}" if not URL.startswith("http") else URL
    bridge_link = f"{base_url}/get/{file_id}"
    try:
        short_link = await get_shortlink(SHORTLINK_URL, SHORTLINK_API, bridge_link)
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
                font-family: 'Poppins', sans-serif;
                background: radial-gradient(circle, #0f2027, #203a43, #2c5364);
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
                background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url('{anime_pic}') no-repeat center center;
                background-size: cover;
                z-index: -1;
                filter: grayscale(50%) blur(5px);
            }}
            .container {{
                background: rgba(0, 0, 0, 0.6);
                padding: 50px;
                border-radius: 30px;
                box-shadow: 0 0 30px rgba(0, 210, 255, 0.5);
                backdrop-filter: blur(25px);
                border: 1px solid rgba(0, 210, 255, 0.3);
                max-width: 500px;
                width: 90%;
                animation: pulse 4s infinite;
            }}
            @keyframes pulse {{
                0% {{ box-shadow: 0 0 20px rgba(0, 210, 255, 0.4); }}
                50% {{ box-shadow: 0 0 50px rgba(0, 210, 255, 0.7); }}
                100% {{ box-shadow: 0 0 20px rgba(0, 210, 255, 0.4); }}
            }}
            .logo {{
                width: 120px;
                height: 120px;
                border-radius: 50%;
                margin-bottom: 25px;
                border: 4px solid #00d2ff;
                object-fit: cover;
                box-shadow: 0 0 20px #00d2ff;
            }}
            h2 {{
                color: #00d2ff;
                margin-bottom: 20px;
                text-shadow: 0 0 15px #00d2ff;
                font-size: 2.5em;
                font-weight: 800;
            }}
            .status {{
                font-size: 1.3em;
                margin-bottom: 30px;
                color: #fff;
                font-weight: 500;
            }}
            .btn {{
                display: inline-block;
                padding: 18px 45px;
                background: linear-gradient(45deg, #00d2ff, #3a7bd5);
                color: white;
                text-decoration: none;
                border-radius: 50px;
                font-weight: 700;
                transition: all 0.4s ease;
                border: none;
                cursor: pointer;
                font-size: 1.2em;
                box-shadow: 0 0 20px rgba(0, 210, 255, 0.6);
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            .btn:hover {{
                transform: scale(1.1);
                box-shadow: 0 0 40px #00d2ff;
            }}
            #timer {{
                font-weight: 800;
                color: #00d2ff;
                font-size: 1.5em;
                text-shadow: 0 0 10px #00d2ff;
            }}
            footer {{
                margin-top: 40px;
                font-size: 1em;
                opacity: 0.8;
                color: #00d2ff;
            }}
            {WATERMARK_STYLE}
        </style>
    </head>
    <body>
        <div class="background"></div>
        {WATERMARK_DIV}
        <div class="container">
            <img src="{anime_pic}" alt="Logo" class="logo">
            <h2>Human Verification</h2>
            <p class="status" id="status_text">✨ Verification Ready! ✧</p>
            <a href="https://t.me/{bot.username}?start={file_id}" class="btn" id="verify_btn">💎 Unlock Now ✧</a>
        </div>
        <script>
            setTimeout(() => {{
                window.location.href = "tg://resolve?domain={bot.username}&start={file_id}";
            }}, 500);
        </script>
        <footer>
            &copy; 2025 {BOT_NAME} | Secure Verification
        </footer>
    </body>
    </html>
    """
    return web.Response(text=html_content, content_type='text/html')
