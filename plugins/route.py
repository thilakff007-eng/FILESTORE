from aiohttp import web
import random
import logging
import time
from config import BOT_NAME, PICS, MAIN_LINK, OWNER_ID, BOT_USERNAME, SHORTLINK_URL, SHORTLINK_API, URL, RECAPTCHA_SITE_KEY, RECAPTCHA_SECRET_KEY
from database.database import db
import aiohttp

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

            // 2. Detect DevTools
            const devtools = {
                isOpen: false,
                orientation: undefined
            };
            const threshold = 160;
            const emitEvent = (isOpen, orientation) => {
                if (isOpen) {
                    IntegrityLockdown("Debugger Detected");
                }
            };
            setInterval(() => {
                const widthThreshold = window.outerWidth - window.innerWidth > threshold;
                const heightThreshold = window.outerHeight - window.innerHeight > threshold;
                const orientation = widthThreshold ? 'vertical' : 'horizontal';
                if (!(heightThreshold && widthThreshold) && ((window.Firebug && window.Firebug.chrome && window.Firebug.chrome.isInitialized) || widthThreshold || heightThreshold)) {
                    if (!devtools.isOpen || devtools.orientation !== orientation) {
                        emitEvent(true, orientation);
                    }
                    devtools.isOpen = true;
                    devtools.orientation = orientation;
                } else {
                    if (devtools.isOpen) {
                        emitEvent(false, undefined);
                    }
                    devtools.isOpen = false;
                    devtools.orientation = undefined;
                }
            }, 500);

            // 3. Detect Userscripts
            const detectionInterval = setInterval(() => {
                if (document.querySelector('textarea[placeholder*="Token will appear here"]') ||
                    document.title.includes("Token Viewer") ||
                    document.getElementById('captcha-token-viewer')) {
                    IntegrityLockdown("Userscript Detected");
                    clearInterval(detectionInterval);
                }
            }, 500);

            // 4. Automation Detection
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

    # Check for empty or suspicious headers
    if not request.headers.get('Accept-Language'):
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

        @keyframes rgb-border {
            0% { border-color: var(--rgb-red); }
            33% { border-color: var(--rgb-blue); }
            66% { border-color: var(--rgb-green); }
            100% { border-color: var(--rgb-red); }
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
            height: 100vh;
            overflow: hidden;
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

        .handshake-row {
            background: #fdfdfd;
            border: 1px solid #eee;
            border-radius: 16px;
            padding: 12px 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 20px;
        }

        .handshake-info {
            display: flex;
            align-items: center;
            font-size: 0.9em;
            color: #555;
        }

        .dot {
            width: 10px;
            height: 10px;
            background: #ff7e5f;
            border-radius: 50%;
            margin-right: 12px;
            box-shadow: 0 0 8px #ff7e5f;
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

        .notice-box {
            background: #fff9db;
            border: 1px solid #ffec99;
            color: #856404;
            padding: 15px;
            border-radius: 12px;
            font-size: 0.85em;
            line-height: 1.4;
            margin-bottom: 20px;
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
        {DETECTION_JS}
        <style>
            .card {{ text-align: center; }}
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
            .card {{ text-align: center; }}
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

    # 1. Sec-Fetch Headers Check (Max Security)
    sec_fetch_site = request.headers.get('Sec-Fetch-Site')
    # logging.info(f"DEBUG: Sec-Fetch-Site: {sec_fetch_site}")
    # Playwright/Local testing might not send this header or might be 'none'
    if sec_fetch_site and sec_fetch_site not in ['same-origin', 'same-site', 'none']:
        logging.warning(f"CSRF/Cross-site attempt detected from IP: {user_ip}")
        return web.Response(text="Security violation: Cross-site request blocked.", status=403)

    # 2. Honeypot Check
    if data.get('sec_field_8x1'):
        logging.warning(f"Honeypot field filled by IP: {user_ip}")
        return web.Response(text="Security validation failed: Bot Activity Detected.", status=403)

    captcha_token = data.get('g-recaptcha-response')
    if not captcha_token:
        return web.Response(text="reCAPTCHA is required", status=403)

    logging.info(f"Visitor IP: {user_ip} attempting verification for token {token}")

    session = request.app.get('http_session')
    if not session:
        # Fallback if session not found for some reason (e.g. testing)
        async with aiohttp.ClientSession() as temp_session:
            async with temp_session.post('https://www.google.com/recaptcha/api/siteverify', data={
                'secret': RECAPTCHA_SECRET_KEY,
                'response': captcha_token,
                'remoteip': user_ip
            }) as resp:
                result = await resp.json()
    else:
        async with session.post('https://www.google.com/recaptcha/api/siteverify', data={
            'secret': RECAPTCHA_SECRET_KEY,
            'response': captcha_token,
            'remoteip': user_ip
        }) as resp:
            result = await resp.json()

    if not result.get('success'):
        return web.Response(text="reCAPTCHA verification failed", status=403)

    # 3. Session Binding (Store IP/UA in DB to verify consistency in next stages)
    await db.update_token_status(token, 'captcha_verified', extra_data={
        'ip': user_ip,
        'ua': request.headers.get('User-Agent')
    })

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Checking Security</title>
        {ANTI_TAMPER_JS}
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
        {RGB_THEME_STYLE}
        <style>
            .progress {{
                height: 8px;
                background: #eee;
                border-radius: 10px;
                overflow: hidden;
                margin: 20px 0;
            }}
            .progress-bar {{
                height: 100%;
                width: 0%;
                background: linear-gradient(90deg, #ff4b2b, #00d2ff, #2ecc71);
                background-size: 200% 100%;
                animation: load 4s linear forwards, rgb-bg-anim 2s linear infinite;
            }}
            @keyframes load {{
                0% {{ width: 0%; }}
                100% {{ width: 100%; }}
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
            // Max Security: Canvas Fingerprinting Detection
            (function() {{
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');
                ctx.textBaseline = "top";
                ctx.font = "14px 'Arial'";
                ctx.textBaseline = "alphabetic";
                ctx.fillStyle = "#f60";
                ctx.fillRect(125,1,62,20);
                ctx.fillStyle = "#069";
                ctx.fillText("BrowserIntegrityCheck", 2, 15);
                ctx.fillStyle = "rgba(102, 204, 0, 0.7)";
                ctx.fillText("BrowserIntegrityCheck", 4, 17);
                const fingerprint = canvas.toDataURL();

                if(fingerprint.length < 100 || navigator.webdriver) {{
                    document.body.innerHTML="<div style='color:red; text-align:center; padding:50px; font-family:Poppins;'><h1>🚫 Security Violation</h1><p>Automated environment detected. Verification aborted.</p></div>";
                    throw new Error("Bot detected");
                }}
            }})();

            if(navigator.webdriver){{
                document.body.innerHTML="Bot access denied";
                throw new Error("Bot detected");
            }}
            if(!navigator.cookieEnabled){{
                alert("Enable cookies to continue");
            }}
            if(window.outerWidth===0){{
                document.body.innerHTML="Suspicious browser detected";
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
    user_ip = get_client_ip(request)
    user_ua = request.headers.get('User-Agent')

    if not token_data or token_data.get('status') != 'captcha_verified':
        return web.Response(text="Access denied. Please complete verification.", status=403)

    # Max Security: Session Binding Consistency Check
    stored_ip = token_data.get('ip')
    stored_ua = token_data.get('ua')
    if stored_ip != user_ip or stored_ua != user_ua:
        logging.warning(f"Session shift detected for token {token}. IP: {stored_ip}->{user_ip}")
        return web.Response(text="Security violation: Session mismatch detected. Please restart verification.", status=403)

    await db.update_token_status(token, 'verified')

    # Increment verify count for the user
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

    # Redirect back to bot
    return web.HTTPFound(location=f"https://t.me/{username}?start={token}")

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
