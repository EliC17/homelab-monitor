from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class MetricIngest(BaseModel):
    target_id: UUID
    metric_name: str
    value: float

class MetricOut(BaseModel):
    id: int
    target_id: UUID
    metric_name: str
    value: float
    recorded_at: datetime

    model_config = {"from_attributes": True}