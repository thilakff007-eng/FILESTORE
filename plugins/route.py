from aiohttp import web
import random
import logging
import time
import asyncio
from config import BOT_NAME, PICS, MAIN_LINK, OWNER_ID, BOT_USERNAME, SHORTLINK_URL, SHORTLINK_API, URL, RECAPTCHA_SITE_KEY, RECAPTCHA_SECRET_KEY
from database.database import db
import aiohttp
from helper_func import get_shortlink

routes = web.RouteTableDef()
verification_attempts = {}

# Advanced Anti-Tamper & Userscript Detection
ANTI_TAMPER_JS = """
    <script>
        (function() {
            // Frame busting
            if (window.self !== window.top) {
                window.top.location = window.self.location;
            }

            const IntegrityLockdown = (reason) => {
                console.error("Integrity Lockdown: " + reason);
                document.documentElement.innerHTML = `
                    <div style="background:#000; color:#ff4444; height:100vh; display:flex; align-items:center; justify-content:center; font-family:sans-serif; text-align:center; padding:20px;">
                        <div>
                            <h1 style="font-size:3em; margin:0;">⚠️ SECURITY ALERT</h1>
                            <h2 style="color:#fff;">Integrity Breach Detected</h2>
                            <p style="color:#ccc; max-width:600px;">Our systems detected an unauthorized modification to this page (${reason}). Verification has been aborted.</p>
                            <p style="color:#ff4444; font-weight:bold;">Action Required: Disable all Userscripts/Extensions and refresh.</p>
                        </div>
                    </div>`;
                window.stop();
            };

            // 1. MutationObserver to catch UI tampering
            const observer = new MutationObserver((mutations) => {
                for (const mutation of mutations) {
                    if (mutation.removedNodes.length > 0) {
                        for (let node of mutation.removedNodes) {
                            if (node.id === 'main-container' || (node.classList && node.classList.contains('card')) || node.nodeName === 'BODY') {
                                IntegrityLockdown("Core UI Element Removed");
                                return;
                            }
                        }
                    }
                    if (mutation.type === 'attributes' && mutation.target.id === 'main-container') {
                        if (mutation.target.style.display === 'none' || mutation.target.style.visibility === 'hidden') {
                            IntegrityLockdown("UI Hidden");
                        }
                    }
                }
            });
            observer.observe(document.documentElement, { childList: true, subtree: true, attributes: true });

            // 2. Detect DevTools (Simple console-based check)
            let devtoolsOpen = false;
            const element = new Image();
            Object.defineProperty(element, 'id', {
                get: function() {
                    devtoolsOpen = true;
                    IntegrityLockdown("Console Open");
                }
            });
            setInterval(() => {
                console.log(element);
            }, 1000);

            // 3. Automation Detection
            if (navigator.webdriver) {
                // Some browsers set this when controlled by automation
                // IntegrityLockdown("Automation detected");
            }
        })();
    </script>
"""

def get_random_pic():
    return random.choice(PICS)

def get_client_ip(request):
    # Try to get the real IP if behind a proxy like Cloudflare or Render
    ip = request.headers.get('CF-Connecting-IP') or \
         request.headers.get('X-Forwarded-For', '').split(',')[0].strip() or \
         request.remote
    return ip

def is_bot(request):
    ua = request.headers.get('User-Agent', '').lower()
    if not ua or len(ua) < 10:
        return True

    blocked_uas = [
        'curl', 'wget', 'python-requests', 'axios', 'headlesschrome',
        'phantomjs', 'selenium', 'puppeteer', 'playwright', 'bot', 'spider',
        'crawl', 'googlebot', 'bingbot', 'yandexbot', 'baiduspider', 'slurp',
        'headless', 'zgrab', 'internet-measurement', 'postman'
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
        })();
    </script>
"""

NEW_LOGO = "https://files.catbox.moe/kyk5ba.jpg"

RGB_THEME_STYLE = """
    <style>
        :root {
            --rgb-white: #ffffff;
            --rgb-red: #ff4b2b;
            --rgb-blue: #00d2ff;
            --rgb-green: #2ecc71;
            --rgb-bg: #f8f9fa;
        }

        @keyframes rgb-shadow {
            0% { box-shadow: 0 10px 30px rgba(255, 75, 43, 0.3); }
            33% { box-shadow: 0 10px 30px rgba(0, 210, 255, 0.3); }
            66% { box-shadow: 0 10px 30px rgba(46, 204, 113, 0.3); }
            100% { box-shadow: 0 10px 30px rgba(255, 75, 43, 0.3); }
        }

        @keyframes rgb-bg-anim {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        body {
            margin: 0; padding: 0;
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(-45deg, #ffffff, #ffccd2, #ccefff, #ccffdb);
            background-size: 400% 400%;
            animation: rgb-bg-anim 15s ease infinite;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
        }

        @keyframes load {
            0% { width: 0%; }
            100% { width: 100%; }
        }

        .card {
            background: white;
            padding: 30px;
            border-radius: 24px;
            width: 90%;
            max-width: 450px;
            text-align: left;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            animation: rgb-shadow 6s infinite;
            position: relative;
        }

        .card-header {
            display: flex;
            align-items: center;
            margin-bottom: 25px;
        }

        .logo-box {
            width: 60px;
            height: 60px;
            background: #111;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 15px;
            padding: 5px;
        }

        .logo-box img {
            max-width: 100%;
            max-height: 100%;
            border-radius: 8px;
        }

        .title-group h2 {
            margin: 0;
            font-size: 1.2em;
            color: #333;
            font-weight: 600;
        }

        .title-group p {
            margin: 0;
            font-size: 0.9em;
            color: #777;
        }

        .continue-btn {
            background: #2ecc71;
            color: white;
            border: none;
            padding: 10px 25px;
            border-radius: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: 0.3s;
        }

        .continue-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(46, 204, 113, 0.4);
        }

        .footer-text {
            text-align: center;
            font-size: 0.75em;
            color: #aaa;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
    </style>
"""

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    if is_bot(request):
        return web.Response(text="Access Denied: Bot Detected 🚫", status=403)
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SecureLink Ultra</title>
        {ANTI_TAMPER_JS}
        {RGB_THEME_STYLE}
        <style>
            .card { text-align: center; }
        </style>
    </head>
    <body>
        <div class="card" id="main-container">
            <div class="card-header" style="justify-content:center; text-align:center; flex-direction:column; margin-right:0;">
                <div class="logo-box" style="margin-right:0; margin-bottom:15px; width:120px; height:120px;">
                    <img src="{NEW_LOGO}" alt="Logo" style="border-radius:20px;">
                </div>
                <div class="title-group">
                    <h1 style="color: #333; font-size: 1.8em; margin: 10px 0;">{BOT_NAME}</h1>
                    <p>Advanced File Store Bot</p>
                </div>
            </div>

            <div style="margin: 30px 0;">
                <a href="{MAIN_LINK}" class="continue-btn" style="text-decoration:none; display:inline-block; padding: 15px 40px;">🚀 Join Community</a>
            </div>

            <div class="footer-text">Protected by reCAPTCHA</div>
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

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>SecureLink Verification</title>
        {ANTI_TAMPER_JS}
        <script src="https://www.google.com/recaptcha/api.js" async defer></script>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;900&display=swap" rel="stylesheet">
        {RGB_THEME_STYLE}
        <style>
            .card { text-align: center; }
        </style>
    </head>
    <body>
        <div class="card" id="main-container">
            <div class="card-header" style="justify-content:center; flex-direction:column; margin-right:0;">
                <div class="logo-box" style="margin-right:0; margin-bottom:15px;">
                    <img src="{NEW_LOGO}" alt="Logo">
                </div>
                <div class="title-group">
                    <h2>SecureLink</h2>
                    <p>Verify to continue</p>
                </div>
            </div>

            <form method="POST" action="/verify/{token}">
                <input type="text" name="sec_field_8x1" style="display:none !important" tabindex="-1" autocomplete="off">

                <div style="text-align:center; margin-bottom:20px;">
                    <div class="g-recaptcha" data-sitekey="{RECAPTCHA_SITE_KEY}" style="display:inline-block;"></div>
                </div>

                <button type="submit" class="continue-btn" style="width:100%">Continue</button>
            </form>

            <div class="footer-text" style="margin-top:20px;">Protected by reCAPTCHA</div>
        </div>
    </body>
    </html>
    """
    return web.Response(text=html_content, content_type='text/html')

@routes.post("/verify/{token}")
async def verify_handler(request):
    if is_bot(request):
        return web.Response(text="Access Denied: Bot Detected 🚫", status=403)

    user_ip = get_client_ip(request)
    now = time.time()

    attempts = verification_attempts.get(user_ip, [])
    attempts = [t for t in attempts if now - t < 60]
    if len(attempts) >= 5:
        return web.Response(text="Too many attempts. Please wait a minute.", status=429)
    attempts.append(now)
    verification_attempts[user_ip] = attempts

    token = request.match_info.get('token')
    data = await request.post()

    if data.get('sec_field_8x1'):
        return web.Response(text="Security validation failed: Bot Activity Detected.", status=403)

    captcha_token = data.get('g-recaptcha-response')
    if not captcha_token:
        return web.Response(text="reCAPTCHA is required", status=403)

    session = request.app.get('http_session')
    async with session.post('https://www.google.com/recaptcha/api/siteverify', data={
        'secret': RECAPTCHA_SECRET_KEY,
        'response': captcha_token,
        'remoteip': user_ip
    }) as resp:
        result = await resp.json()

    if not result.get('success'):
        return web.Response(text="reCAPTCHA verification failed", status=403)

    await db.update_token_status(token, 'captcha_verified', extra_data={
        'ip': user_ip,
        'ua': request.headers.get('User-Agent')
    })

    # Generate Shortlink for the next stage
    base_url = f"https://{URL}" if not URL.startswith("http") else URL
    final_go_link = f"{base_url}/go/{token}"

    # Clean SHORTLINK_URL to remove trailing slash for Shortzy
    clean_short_url = SHORTLINK_URL.strip().rstrip('/')
    short_link = await get_shortlink(clean_short_url, SHORTLINK_API, final_go_link)

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Checking Security</title>
        {ANTI_TAMPER_JS}
        {DETECTION_JS}
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
        {RGB_THEME_STYLE}
        <style>
            .progress {{
                height: 12px;
                background: #f0f0f0;
                border-radius: 10px;
                overflow: hidden;
                margin: 25px 0;
                border: 1px solid #eee;
            }}
            .progress-bar {{
                height: 100%;
                width: 0%;
                background: linear-gradient(90deg, #ff4b2b, #00d2ff, #2ecc71);
                background-size: 200% 100%;
                animation: load 4s cubic-bezier(0.4, 0, 0.2, 1) forwards, rgb-bg-anim 3s linear infinite;
                display: block !important;
                visibility: visible !important;
                border-radius: 10px;
            }}
            h2 {{ margin-bottom: 5px; color: #333; }}
            p {{ color: #666; margin: 0; }}
            .subtitle {{ font-size: 0.85em; color: #888; margin-top: 10px; }}
        </style>
    </head>
    <body>
        <div class="card" id="main-container" style="text-align: center;">
            <div class="logo-box" style="margin: 0 auto 20px;">
                <img src="{NEW_LOGO}" alt="Logo">
            </div>
            <h2>Checking Security</h2>
            <p>Please wait…</p>

            <div class="progress">
                <div class="progress-bar"></div>
            </div>

            <p class="subtitle">Verifying Browser Integrity</p>
        </div>
        <script>
            // Safety: Ensure we redirect even if JS integrity checks fail silently
            function finish() {{
                window.location.href = "{short_link}";
            }}

            try {{
                // Integrity check: Cookies
                if(!navigator.cookieEnabled){{
                    alert("Enable cookies to continue");
                }}

                // Integrity check: Screen dimensions (basic bot check)
                if(window.outerWidth === 0 && !/Android|iPhone|iPad|iPod/i.test(navigator.userAgent)){{
                     document.body.innerHTML="Suspicious browser detected";
                     throw new Error("Bot dimension check failed");
                }}

                setTimeout(finish, 4500);
            }} catch(e) {{
                console.error(e);
                // Allow redirect anyway as fallback for real users with strict privacy settings
                setTimeout(finish, 5000);
            }}
        </script>
    </body>
    </html>
    """
    return web.Response(text=html_content, content_type='text/html')

@routes.get("/go/{token}")
async def final_redirect_handler(request):
    if is_bot(request):
        return web.Response(text="Access Denied: Bot Detected 🚫", status=403)

    token = request.match_info.get('token')
    token_data = await db.get_verify_token(token)
    user_ip = get_client_ip(request)

    if not token_data or token_data.get('status') != 'captcha_verified':
        return web.Response(text="Access denied. Please complete verification.", status=403)

    # Session consistency check
    if token_data.get('ip') != user_ip:
        logging.warning(f"IP Mismatch for token {token}: {token_data.get('ip')} vs {user_ip}")
        # Relaxing this for now to avoid issues with some mobile network transitions
        # return web.Response(text="Security mismatch detected. Please restart.", status=403)

    await db.update_token_status(token, 'verified')

    # Update verify count
    try:
        user_id = token_data.get('user_id')
        if user_id:
            count = await db.get_verify_count(user_id)
            await db.set_verify_count(user_id, count + 1)
            await db.update_verify_status(user_id, is_verified=True, verified_time=time.time())
    except Exception as e:
        logging.error(f"Error updating verify status: {e}")

    bot = request.app.get('bot')
    username = bot.username if bot and hasattr(bot, 'username') and bot.username else BOT_USERNAME

    return web.HTTPFound(location=f"https://t.me/{username}?start={token}")
