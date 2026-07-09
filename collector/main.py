import os
import asyncio
import aiohttp
import requests
import logging
from poll_server import start_poll_server, set_poll_callback

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
logger = logging.getLogger(__name__)

API_BASE = os.environ.get("API_BASE", "http://localhost:8000/api/v1")
COLLECTOR_SECRET = os.environ.get("COLLECTOR_SECRET", "")
HEADERS = {"x-collector-secret": COLLECTOR_SECRET}

CREDENTIALS_BY_TARGET_TYPE = {
    "proxmox_host": {
        "user": os.environ.get("PROXMOX_USER", "root@pam"),
        "token_name": os.environ.get("PROXMOX_TOKEN_NAME", "monitor"),
        "token_value": os.environ.get("PROXMOX_TOKEN_VALUE", ""),
        "node_name": os.environ.get("PROXMOX_NODE_NAME", "pve"),
    },
}

running_targets = {}
target_registry = {}  # target_id -> target dict

def fetch_targets():
    try:
        resp = requests.get(f"{API_BASE}/internal/targets", headers=HEADERS)
        resp.raise_for_status()
        data = resp.json()
        if not isinstance(data, list):
            logger.error(f"Unexpected targets response: {data}")
            return []
        return data
    except Exception as e:
        logger.error(f"Failed to fetch targets: {e}")
        return []

async def poll_target_now(target_id: str):
    """Called by poll server for manual/immediate polls."""
    target = target_registry.get(target_id)
    if not target:
        logger.warning(f"Poll requested for unknown target: {target_id}")
        return
    from scheduler import poll_target
    async with aiohttp.ClientSession() as session:
        await poll_target(session, target, CREDENTIALS_BY_TARGET_TYPE.get(target["target_type"]))

async def reconcile_loop(session):
    from scheduler import target_loop
    while True:
        targets = {t["id"]: t for t in fetch_targets() if t["enabled"]}
        target_registry.update(targets)
        logger.info(f"Reconcile: {len(targets)} active targets")
        for tid, t in targets.items():
            if tid not in running_targets:
                credential = CREDENTIALS_BY_TARGET_TYPE.get(t["target_type"])
                running_targets[tid] = asyncio.create_task(target_loop(session, t, credential))
        for tid in list(running_targets):
            if tid not in targets:
                running_targets[tid].cancel()
                del running_targets[tid]
            target_registry.pop(tid, None)
        await asyncio.sleep(60)

async def wait_for_api():
    api_root = API_BASE.replace("/api/v1", "")
    for i in range(30):
        try:
            resp = requests.get(f"{api_root}/health", timeout=2)
            if resp.status_code == 200:
                logger.info("API is ready")
                return
        except Exception:
            pass
        logger.info(f"Waiting for API... attempt {i+1}/30")
        await asyncio.sleep(10)
    raise RuntimeError("API never became ready")

async def main():
    set_poll_callback(poll_target_now)
    await start_poll_server()
    await wait_for_api()
    async with aiohttp.ClientSession() as session:
        await reconcile_loop(session)

if __name__ == "__main__":
    asyncio.run(main())