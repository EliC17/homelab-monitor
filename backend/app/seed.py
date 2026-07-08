from sqlalchemy.orm import Session
from app.core.db import SessionLocal
from app.models.target import Target

SEED_TARGETS = [
    {
        "name": "pve-host-01",
        "target_type": "proxmox_host",
        "hostname": "192.168.0.68",
        "poll_interval_s": 30,
        "enabled": True,
    },
    {
        "name": "my-docker-host",
        "target_type": "docker_host",
        "hostname": "192.168.0.145",
        "poll_interval_s": 15,
        "enabled": True,
    },
    {
        "name": "managed-switch",
        "target_type": "generic",
        "hostname": "192.168.0.2",
        "poll_interval_s": 30,
        "enabled": True,
    },
]

def seed_targets():
    db: Session = SessionLocal()
    try:
        for t in SEED_TARGETS:
            exists = db.query(Target).filter_by(name=t["name"]).first()
            if not exists:
                db.add(Target(**t))
                print(f"Seeded target: {t['name']}")
            else:
                print(f"Target already exists, skipping: {t['name']}")
        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    seed_targets()