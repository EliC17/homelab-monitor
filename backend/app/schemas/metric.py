from uuid import UUID
from pydantic import BaseModel

class MetricIngest(BaseModel):
    target_id: UUID
    metric_name: str
    value: float