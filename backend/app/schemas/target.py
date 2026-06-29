from enum import Enum
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
 
class TargetType(str, Enum):
    proxmox_host = "proxmox_host"
    lxc = "lxc"
    vm = "vm"
    docker_host = "docker_host"
    generic = "generic"
 
class TargetCreate(BaseModel):
    name: str
    target_type: TargetType
    hostname: str
    credential_id: UUID | None = None
    poll_interval_s: int = 60
 
class TargetOut(TargetCreate):
    id: UUID
    enabled: bool
    created_at: datetime
 
    class Config:
        from_attributes = True
