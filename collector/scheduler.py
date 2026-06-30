import asyncio, aiohttp
from adapters.docker_adapter import DockerAdapter
from adapters.proxmox_adapter import ProxmoxAdapter
from adapters.generic_adapter import GenericAdapter

ADAPTERS = {
    "docker_host": DockerAdapter(),
    "proxmox_host": ProxmoxAdapter(),
    "generic": GenericAdapter()
}
API_BASE = "http://localhost:8000/api/v1"

async def poll_target(session, target, credential):
    adapter = ADAPTERS[target["target_type"]]
    points = await adapter.collect(target, credential)
    payload = [
        {"target_id": target["id"], "metric_name": pt.metric_name, "value": pt.value}
        for pt in points
    ]
    await session.post(f"{API_BASE}/metrics/ingest", json=payload)
    return points[0].value == 1 if points[0].metric_name == "reachable" else True

async def target_loop(session, target, credential):
    consecutive_failures = 0
    while True:
        ok = await poll_target(session, target, credential)
        if ok:
            consecutive_failures = 0
            delay = target["poll_interval_s"]
        else:
            consecutive_failures += 1
            delay = min(target["poll_interval_s"] * (2 ** consecutive_failures), 600)
        await asyncio.sleep(delay)