import asyncio
import requests
from scheduler import target_loop

API_BASE = "http://localhost:8000/api/v1"

# TEMPORARY — replace with real Credential lookups in Milestone 6
CREDENTIALS_BY_TARGET_TYPE = {
    "proxmox_host": {
        "user": "root@pam",
        "token_name": "monitor",
        "token_value": "0348d2fc-97f8-45f6-84f0-64296d1bc9dd",
        "node_name": "pve", 
    },
}

running_targets = {}   # target_id -> asyncio.Task

def fetch_targets():
    return requests.get(f"{API_BASE}/targets").json()

async def reconcile_loop(session, fetch_targets, interval=60):
    while True:
        targets = {t["id"]: t for t in fetch_targets() if t["enabled"]}
        for tid, t in targets.items():
            if tid not in running_targets:
                credential = CREDENTIALS_BY_TARGET_TYPE.get(t["target_type"])
                running_targets[tid] = asyncio.create_task(target_loop(session, t, credential))
        for tid in list(running_targets):
            if tid not in targets:
                running_targets[tid].cancel()
                del running_targets[tid]
        await asyncio.sleep(interval)

async def main():
    import aiohttp
    async with aiohttp.ClientSession() as session:
        await reconcile_loop(session, fetch_targets)

if __name__ == "__main__":
    asyncio.run(main())