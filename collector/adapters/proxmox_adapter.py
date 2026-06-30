from proxmoxer import ProxmoxAPI
from .base import Adapter, MetricPoint

class ProxmoxAdapter(Adapter):
    async def collect(self, target, credential):
        try:
            import asyncio
            return await asyncio.to_thread(self._collect_sync, target, credential)
        except Exception:
            return [MetricPoint("reachable", 0)]

    def _collect_sync(self, target, credential):
        proxmox = ProxmoxAPI(
            target["hostname"], user=credential["user"],
            token_name=credential["token_name"], token_value=credential["token_value"],
            verify_ssl=False,
        )
        node = proxmox.nodes(credential["node_name"]).status.get()
        return [
            MetricPoint("reachable", 1),
            MetricPoint("cpu_pct", node["cpu"] * 100),
            MetricPoint("mem_pct", node["memory"]["used"] / node["memory"]["total"] * 100),
        ]