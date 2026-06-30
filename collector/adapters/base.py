from abc import ABC, abstractmethod
from dataclasses import dataclass
 
@dataclass
class MetricPoint:
    metric_name: str
    value: float
 
class Adapter(ABC):
    """One adapter per target_type. Must not raise on connection failure —
    catch and return a synthetic reachable=0 point instead, so the scheduler
    never has to special-case adapter exceptions."""
 
    @abstractmethod
    async def collect(self, target: dict, credential: dict | None) -> list[MetricPoint]:
        ...
