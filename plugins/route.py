from aiohttp import web
import random
import logging
import time
from config import BOT_NAME, PICS, MAIN_LINK, OWNER_ID, BOT_USERNAME, SHORTLINK_URL, SHORTLINK_API, URL, RECAPTCHA_SITE_KEY, RECAPTCHA_SECRET_KEY
from database.database import db
import aiohttp

routes = web.RouteTableDef()
verification_attempts = {}

def get_random_pic():
    return random.choice(PICS)

def is_bot(request):
    ua = request.headers.get('User-Agent', '').lower()
    blocked_uas = [
        'curl', 'wget', 'python-requests', 'axios', 'headlesschrome',
        'phantomjs', 'selenium', 'puppeteer', 'playwright', 'bot', 'spider', 'crawl'
    ]
    for agent in blocked_uas:
        if agent in ua:
            return True
    return False

DETECTION_JS = """
    <script>
        (function() {
            const isHeadless = /HeadlessChrome/.test(navigator.userAgent) || navigator.webdriver;
            const isPhantom = /PhantomJS/.test(navigator.userAgent);
            const isChrome = /Chrome/.test(navigator.userAgent) && /Google Inc/.test(navigator.vendor);

            if (isHeadless || isPhantom) {
                document.body.innerHTML = '<div style="color:red; font-size:24px; padding:50px;">🚫 Automation Detected! Please use a real browser (Chrome recommended). 🏯</div>';
                throw new Error("Bot detected");
            }

            if (!isChrome && !/Android|iPhone|iPad|iPod/i.test(navigator.userAgent)) {
                // Not enforcing Chrome on mobile, but for desktop we want Chrome-like
                console.warn("Browser not verified, Chrome is recommended.");
            }
        })();
    </script>
"""

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

WATERMARK_DIV = f'<div class="watermark">{BOT_NAME}</div>'

ANIME_COMMON_STYLE = f"""
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
                background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url('{{anime_pic}}') no-repeat center center;
                background-size: cover;
                z-index: -1;
                filter: blur(5px);
                transform: scale(1.1);
            }}
            .container {{
                background: rgba(0, 0, 0, 0.6);
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 0 20px #e94560;
                backdrop-filter: blur(10px);
                border: 2px solid #e94560;
                max-width: 450px;
                width: 90%;
            }}
            .logo {{
                width: 120px;
                height: 120px;
                border-radius: 50%;
                margin-bottom: 20px;
                border: 3px solid #e94560;
                object-fit: cover;
                box-shadow: 0 0 15px #e94560;
            }}
            h1 {{ color: #e94560; text-shadow: 0 0 10px #e94560; }}
            .btn {{
                display: inline-block;
                padding: 12px 30px;
                background: #e94560;
                color: white;
                text-decoration: none;
                border-radius: 30px;
                font-weight: bold;
                transition: 0.3s;
                border: none;
                cursor: pointer;
                box-shadow: 0 0 10px #e94560;
            }}
            .btn:hover {{ transform: scale(1.05); box-shadow: 0 0 20px #e94560; }}
            {WATERMARK_STYLE}
        </style>
"""

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    if is_bot(request):
        return web.Response(text="Access Denied: Bot Detected 🚫", status=403)
    anime_pic = get_random_pic()
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{BOT_NAME}</title>
        {ANIME_COMMON_STYLE.replace('{{anime_pic}}', anime_pic)}
        {DETECTION_JS}
    </head>
    <body>
        <div class="background"></div>
        {WATERMARK_DIV}
        <div class="container">
            <img src="{anime_pic}" class="logo">
            <h1>{BOT_NAME}</h1>
            <p>Advanced File Store Bot</p>
            <a href="{MAIN_LINK}" class="btn">🚀 Join Community</a>
        </div>
    </body>
    </html>
    """
    return web.Response(text=html_content, content_type='text/html')

@routes.get("/task/{token}")
async def task_handler(request):
    if is_bot(request):
        return web.Response(text="Access Denied: Bot Detected 🚫", status=403)
    token = request.match_info.get('token')
    token_data = await db.get_verify_token(token)
    if not token_data:
        return web.Response(text="Invalid or expired token", status=403)

    anime_pic = get_random_pic()
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>SecureLink Verification</title>
        <script src="https://www.google.com/recaptcha/api.js" async defer></script>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;900&display=swap" rel="stylesheet">
        <style>
            body {{
                margin: 0; padding: 0;
                font-family: 'Poppins', sans-serif;
                background: radial-gradient(circle, #1a1a2e, #16213e, #0f3460);
                color: white;
                display: flex;
                align-items: center;
                justify-content: center;
                height: 100vh;
                overflow: hidden;
            }}
            .background {{
                position: fixed;
                top: 0; left: 0; width: 100%; height: 100%;
                background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url('{anime_pic}') no-repeat center center;
                background-size: cover;
                z-index: -1;
                filter: blur(8px);
                transform: scale(1.1);
            }}
            .card {{
                background: rgba(0, 0, 0, 0.7);
                padding: 40px;
                border-radius: 20px;
                width: 350px;
                text-align: center;
                box-shadow: 0 0 25px #e94560, inset 0 0 10px #e94560;
                backdrop-filter: blur(15px);
                border: 2px solid #e94560;
                animation: neonPulse 2s infinite alternate;
            }}
            @keyframes neonPulse {{
                from {{ box-shadow: 0 0 20px #e94560; }}
                to {{ box-shadow: 0 0 40px #e94560, 0 0 10px #e94560; }}
            }}
            h2 {{
                color: #e94560;
                text-shadow: 0 0 10px #e94560, 0 0 20px #e94560;
                font-weight: 900;
                font-size: 2em;
                margin-top: 0;
            }}
            p {{ color: #ccc; margin-bottom: 25px; }}
            .chrome-notice {{
                font-size: 0.8em;
                color: #ffcc00;
                margin-top: 15px;
                font-weight: bold;
                text-shadow: 0 0 5px rgba(255, 204, 0, 0.5);
            }}
            button {{
                background: #e94560;
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 30px;
                cursor: pointer;
                font-size: 16px;
                font-weight: bold;
                margin-top: 20px;
                transition: 0.3s;
                box-shadow: 0 0 15px #e94560;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            button:hover {{
                transform: scale(1.05);
                box-shadow: 0 0 25px #e94560;
            }}
            .g-recaptcha {{
                display: inline-block;
                margin-bottom: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="background"></div>
        <div class="card">
            <h2>SecureLink</h2>
            <p>Verify to continue, Senpai! 🌸</p>
            <form method="POST" action="/verify/{token}">
                <div class="g-recaptcha" data-sitekey="{RECAPTCHA_SITE_KEY}"></div>
                <br>
                <button type="submit">Continue 🚀</button>
            </form>
            <div class="chrome-notice">⚠️ Verification works in Chrome browser only!</div>
        </div>
    </body>
    </html>
    """
    return web.Response(text=html_content, content_type='text/html')

@routes.post("/verify/{token}")
async def verify_handler(request):
    if is_bot(request):
        return web.Response(text="Access Denied: Bot Detected 🚫", status=403)

    user_ip = request.remote
    now = time.time()
    # Simple Rate Limiting: 5 attempts per minute per IP
    attempts = verification_attempts.get(user_ip, [])
    attempts = [t for t in attempts if now - t < 60]
    if len(attempts) >= 5:
        return web.Response(text="Too many attempts. Please wait a minute.", status=429)
    attempts.append(now)
    verification_attempts[user_ip] = attempts

    # Periodically clean up old entries to prevent memory leak
    if random.random() < 0.05:
        expired_cutoff = now - 60
        for ip in list(verification_attempts.keys()):
            verification_attempts[ip] = [t for t in verification_attempts[ip] if t > expired_cutoff]
            if not verification_attempts[ip]:
                del verification_attempts[ip]

    token = request.match_info.get('token')
    data = await request.post()
    captcha_token = data.get('g-recaptcha-response')
    user_ip = request.remote

    logging.info(f"Visitor IP: {user_ip} attempting verification for token {token}")

    if not captcha_token:
        return web.Response(text="reCAPTCHA is required", status=403)

    async with aiohttp.ClientSession() as session:
        async with session.post('https://www.google.com/recaptcha/api/siteverify', data={
            'secret': RECAPTCHA_SECRET_KEY,
            'response': captcha_token,
            'remoteip': user_ip
        }) as resp:
            result = await resp.json()

    if not result.get('success'):
        return web.Response(text="reCAPTCHA verification failed", status=403)

    await db.update_token_status(token, 'captcha_verified')

    anime_pic = get_random_pic()
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Checking Security</title>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;900&display=swap" rel="stylesheet">
        <style>
            body {{
                margin: 0; padding: 0;
                font-family: 'Poppins', sans-serif;
                background: radial-gradient(circle, #1a1a2e, #16213e, #0f3460);
                color: white;
                display: flex;
                align-items: center;
                justify-content: center;
                height: 100vh;
                overflow: hidden;
            }}
            .background {{
                position: fixed;
                top: 0; left: 0; width: 100%; height: 100%;
                background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url('{anime_pic}') no-repeat center center;
                background-size: cover;
                z-index: -1;
                filter: blur(8px);
                transform: scale(1.1);
            }}
            .card {{
                background: rgba(0, 0, 0, 0.7);
                padding: 40px;
                border-radius: 20px;
                width: 350px;
                text-align: center;
                box-shadow: 0 0 25px #00d2ff, inset 0 0 10px #00d2ff;
                backdrop-filter: blur(15px);
                border: 2px solid #00d2ff;
                animation: neonPulseBlue 2s infinite alternate;
            }}
            @keyframes neonPulseBlue {{
                from {{ box-shadow: 0 0 20px #00d2ff; }}
                to {{ box-shadow: 0 0 40px #00d2ff, 0 0 10px #00d2ff; }}
            }}
            .progress {{
                height: 8px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                overflow: hidden;
                margin-top: 25px;
                border: 1px solid rgba(0, 210, 255, 0.3);
            }}
            .progress-bar {{
                height: 100%;
                width: 0%;
                background: linear-gradient(90deg, #00d2ff, #3a7bd5);
                animation: load 4s linear forwards;
                box-shadow: 0 0 15px #00d2ff;
            }}
            @keyframes load {{
                0% {{ width: 0% }}
                100% {{ width: 100% }}
            }}
            h2 {{
                color: #00d2ff;
                text-shadow: 0 0 10px #00d2ff, 0 0 20px #00d2ff;
                font-weight: 900;
                margin-bottom: 10px;
            }}
            p {{ color: #ccc; margin: 5px 0; }}
            .subtitle {{ font-size: 0.9em; color: #3a7bd5; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; }}
            .chrome-notice {{
                font-size: 0.8em;
                color: #ffcc00;
                margin-top: 20px;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="background"></div>
        <div class="card">
            <h2>Checking Security</h2>
            <p>Please wait, Senpai… 🌸</p>
            <p class="subtitle">Verifying Browser Integrity</p>
            <div class="progress">
                <div class="progress-bar"></div>
            </div>
            <div class="chrome-notice">⚠️ Chrome Browser required for this step!</div>
        </div>
        <script>
            if(navigator.webdriver){{
                document.body.innerHTML="<div style='color:white; text-align:center; padding:50px; font-family:Poppins;'><h1>🚫 Bot Access Denied</h1><p>Please use a real Chrome browser.</p></div>";
                throw new Error("Bot detected");
            }}
            if(!navigator.cookieEnabled){{
                alert("Enable cookies to continue");
            }}
            if(window.outerWidth===0){{
                document.body.innerHTML="<div style='color:white; text-align:center; padding:50px; font-family:Poppins;'><h1>⚠️ Suspicious Browser</h1><p>Verification failed.</p></div>";
                throw new Error("Suspicious browser");
            }}

            setTimeout(function(){{
                window.location.href="/task_done/{token}";
            }}, 4000);
        </script>
    </body>
    </html>
    """
    return web.Response(text=html_content, content_type='text/html')

@routes.get("/task_done/{token}")
async def task_done_handler(request):
    token = request.match_info.get('token')
    token_data = await db.get_verify_token(token)

    if not token_data or token_data.get('status') != 'captcha_verified':
        return web.Response(text="Access denied. Please complete verification.", status=403)

    await db.update_token_status(token, 'task_done')
    base_url = f"https://{URL}" if not URL.startswith("http") else URL
    return web.HTTPFound(location=f"{base_url}/link/__{OWNER_ID}__/{token}")

@routes.get(f"/link/__{OWNER_ID}__" + "/{token}")
async def redirect_handler(request):
    token = request.match_info.get('token')
    token_data = await db.get_verify_token(token)
    if not token_data or token_data.get('status') != 'task_done':
        return web.Response(text="Bypassing detected or invalid session.", status=403)

    from helper_func import get_shortlink
    base_url = f"https://{URL}" if not URL.startswith("http") else URL
    bridge_link = f"{base_url}/hold/{token}"

    try:
        short_link = await get_shortlink(SHORTLINK_URL, SHORTLINK_API, bridge_link)
        return web.HTTPFound(location=short_link)
    except Exception as e:
        logging.error(f"Shortlink error: {e}")
        return web.HTTPFound(location=bridge_link)

@routes.get("/hold/{token}")
async def hold_handler(request):
    if is_bot(request):
        return web.Response(text="Access Denied: Bot Detected 🚫", status=403)
    token = request.match_info.get('token')
    token_data = await db.get_verify_token(token)
    if not token_data:
        return web.Response(text="Invalid token", status=403)

    anime_pic = get_random_pic()
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Final Verification</title>
        {ANIME_COMMON_STYLE.replace('{{anime_pic}}', anime_pic)}
        {DETECTION_JS}
        <style>
            #hold-btn {{
                width: 200px;
                height: 200px;
                border-radius: 50%;
                background: #e94560;
                border: 10px solid rgba(255, 255, 255, 0.1);
                color: white;
                font-size: 20px;
                font-weight: bold;
                cursor: pointer;
                user-select: none;
                transition: transform 0.2s, box-shadow 0.2s;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 20px auto;
                position: relative;
            }}
            #hold-btn:active {{ transform: scale(0.95); }}
            #progress-ring {{
                position: absolute;
                top: -10px; left: -10px;
                width: 200px; height: 200px;
            }}
            .loading-dots:after {{
                content: ' .';
                animation: dots 1s steps(5, end) infinite;
            }}
            @keyframes dots {{
                0%, 20% {{ color: rgba(0,0,0,0); text-shadow: .25em 0 0 rgba(0,0,0,0), .5em 0 0 rgba(0,0,0,0); }}
                40% {{ color: white; text-shadow: .25em 0 0 rgba(0,0,0,0), .5em 0 0 rgba(0,0,0,0); }}
                60% {{ text-shadow: .25em 0 0 white, .5em 0 0 rgba(0,0,0,0); }}
                80%, 100% {{ text-shadow: .25em 0 0 white, .5em 0 0 white; }}
            }}
        </style>
    </head>
    <body>
        <div class="background"></div>
        <div class="container">
            <h1>Hold to Verify</h1>
            <p>Almost there! Hold the button for 5 seconds to get your files. 🌸</p>
            <div id="hold-btn">Hold Me</div>
            <p id="timer-text">Wait: 5.0s</p>
        </div>

        <script>
            let btn = document.getElementById('hold-btn');
            let text = document.getElementById('timer-text');
            let timer = null;
            let startTime = 0;
            let duration = 5000;

            function startHold(e) {{
                e.preventDefault();
                startTime = Date.now();
                btn.style.boxShadow = "0 0 50px #e94560";
                timer = setInterval(updateTimer, 100);
            }}

            function endHold() {{
                clearInterval(timer);
                btn.style.boxShadow = "0 0 10px #e94560";
                text.innerText = "Wait: 5.0s";
            }}

            function updateTimer() {{
                let elapsed = Date.now() - startTime;
                let remaining = Math.max(0, (duration - elapsed) / 1000);
                text.innerText = "Wait: " + remaining.toFixed(1) + "s";

                if (elapsed >= duration) {{
                    clearInterval(timer);
                    verify();
                }}
            }}

            async function verify() {{
                btn.innerText = "Verifying...";
                btn.disabled = true;
                let res = await fetch('/complete_hold/{token}', {{method: 'POST'}});
                if (res.ok) {{
                    window.location.href = '/get/{token}';
                }} else {{
                    alert("Verification Failed! Try Again.");
                    location.reload();
                }}
            }}

            btn.addEventListener('mousedown', startHold);
            btn.addEventListener('touchstart', startHold);
            window.addEventListener('mouseup', endHold);
            window.addEventListener('touchend', endHold);
        </script>
    </body>
    </html>
    """
    return web.Response(text=html_content, content_type='text/html')

@routes.post("/complete_hold/{token}")
async def complete_hold_handler(request):
    token = request.match_info.get('token')
    token_data = await db.get_verify_token(token)
    if not token_data:
        return web.Response(status=403)

    await db.update_token_status(token, 'verified')

    # Increment verify count for the user (for /stats and daily reporting)
    try:
        user_id = token_data.get('user_id')
        if user_id:
            count = await db.get_verify_count(user_id)
            await db.set_verify_count(user_id, count + 1)

            # Update user's verified status for 24h persistence
            await db.update_verify_status(user_id, is_verified=True, verified_time=time.time())
    except Exception as e:
        logging.error(f"Error updating verify status: {e}")

    return web.Response(status=200)

@routes.get("/get/{token}")
async def get_route_handler(request):
    token = request.match_info.get('token')
    bot = request.app.get('bot')
    username = bot.username if bot and hasattr(bot, 'username') and bot.username else BOT_USERNAME

    # Check if fully verified
    token_data = await db.get_verify_token(token)
    if not token_data or token_data.get('status') != 'verified':
        return web.Response(text="Not verified", status=403)

    logging.info(f"Redirecting verified user back to bot {username} with token {token}")
    return web.HTTPFound(location=f"https://t.me/{username}?start={token}")
