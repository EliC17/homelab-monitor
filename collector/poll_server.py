import asyncio
import os
from aiohttp import web
import logging

logger = logging.getLogger(__name__)

COLLECTOR_SECRET = os.environ.get("COLLECTOR_SECRET", "")

# reference to running_targets from main.py — injected on startup
_poll_callback = None

def set_poll_callback(callback):
    global _poll_callback
    _poll_callback = callback

async def handle_poll(request):
    secret = request.headers.get("x-collector-secret", "")
    if secret != COLLECTOR_SECRET:
        return web.Response(status=403, text="Forbidden")
    target_id = request.match_info["target_id"]
    if _poll_callback:
        await _poll_callback(target_id)
        return web.json_response({"status": "ok"})
    return web.json_response({"status": "no callback"}, status=503)

async def start_poll_server():
    app = web.Application()
    app.router.add_post("/poll/{target_id}", handle_poll)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 9000)
    await site.start()
    logger.info("Poll server listening on :9000")