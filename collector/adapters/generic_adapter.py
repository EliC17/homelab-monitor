from icmplib import async_ping
from .base import Adapter, MetricPoint
 
class GenericAdapter(Adapter):
    async def collect(self, target, credential):
        host = await async_ping(target["hostname"], count=3, timeout=2)
        if not host.is_alive:
            return [MetricPoint("reachable", 0)]
        points = [MetricPoint("reachable", 1), MetricPoint("latency_ms", host.avg_rtt)]
        # SNMP OID polling (e.g. for a switch/NAS) added here if credential has community string
        return points
