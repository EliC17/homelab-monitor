import docker
from .base import Adapter, MetricPoint
 
class DockerAdapter(Adapter):
    async def collect(self, target, credential):
        try:
            url = f"tcp://{target['hostname']}:2375"
            client = docker.DockerClient(base_url=url)
            containers = client.containers.list(all=True)
            running = sum(1 for c in containers if c.status == "running")
            points = [
                MetricPoint("reachable", 1),
                MetricPoint("containers_total", len(containers)),
                MetricPoint("containers_running", running),
            ]
            # per-container CPU/mem stats can be added here via container.stats()
            return points
        except Exception:
            return [MetricPoint("reachable", 0)]
