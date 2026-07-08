import asyncio
import aiohttp
import os
import logging

logger = logging.getLogger(__name__)

API_BASE = os.environ.get("API_BASE", "http://localhost:8000/api/v1")
COLLECTOR_SECRET = os.environ.get("COLLECTOR_SECRET", "")
HEADERS = {"x-collector-secret": COLLECTOR_SECRET}

from adapters.docker_adapter import DockerAdapter
from adapters.proxmox_adapter import ProxmoxAdapter
from adapters.generic_adapter import GenericAdapter

ADAPTERS = {
    "docker_host": DockerAdapter(),
    "proxmox_host": ProxmoxAdapter(),
    "generic": GenericAdapter(),
}

async def poll_target(session, target, credential):
    logger.info(f"Polling {target['name']} ({target['target_type']})")
    adapter = ADAPTERS.get(target["target_type"])
    if not adapter:
        logger.error(f"No adapter for target type: {target['target_type']}")
        return False
    points = await adapter.collect(target, credential)
    logger.info(f"  -> {target['name']}: {[(p.metric_name, p.value) for p in points]}")
    payload = [
        {"target_id": target["id"], "metric_name": pt.metric_name, "value": pt.value}
        for pt in points
    ]
    async with session.post(f"{API_BASE}/metrics/ingest", json=payload,
                            headers=HEADERS) as resp:
        status = resp.status
        logger.info(f"  -> ingest response: {status}")
        return status == 201 and points[0].value == 1

async def target_loop(session, target, credential):
    consecutive_failures = 0
    while True:
        try:
            ok = await poll_target(session, target, credential)
            if ok:
                consecutive_failures = 0
                delay = target["poll_interval_s"]
            else:
                consecutive_failures += 1
                delay = min(target["poll_interval_s"] * (2 ** consecutive_failures), 600)
        except Exception as e:
            import logging
            logging.getLogger(__name__).error(f"target_loop error for {target['name']}: {e}", exc_info=True)
            consecutive_failures += 1
            delay = min(target["poll_interval_s"] * (2 ** consecutive_failures), 600)
        await asyncio.sleep(delay)