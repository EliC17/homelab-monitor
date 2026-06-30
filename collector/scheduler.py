import asyncio, aiohttp
from adapters.docker_adapter import DockerAdapter
 
ADAPTERS = {"docker_host": DockerAdapter()}
API_BASE = "http://localhost:8000/api/v1"
 
async def poll_target(session, target):
    adapter = ADAPTERS[target["target_type"]]
    points = await adapter.collect(target, None)
    payload = [
        {"target_id": target["id"], "metric_name": pt.metric_name, "value": pt.value}
        for pt in points
    ]
    await session.post(f"{API_BASE}/metrics/ingest", json=payload)
 
async def target_loop(session, target):
    while True:
        await poll_target(session, target)
        await asyncio.sleep(target["poll_interval_s"])
 
async def run(targets):
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*(target_loop(session, t) for t in targets))
