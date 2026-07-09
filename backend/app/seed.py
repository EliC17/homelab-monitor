from sqlalchemy.orm import Session
from app.core.db import SessionLocal
from app.models.target import Target
from app.models.alert import AlertRule
import uuid

SEED_RULES = [
    {
        "target_name": "my-docker-host",  # resolved to ID below
        "metric_name": "reachable",
        "comparator": "eq",
        "threshold": 0.0,
        "duration_s": 0,
        "severity": "critical",
        "cooldown_s": 60,
        "enabled": True,
    },
    {
        "target_name": "pve-host-01",
        "metric_name": "reachable",
        "comparator": "eq",
        "threshold": 0.0,
        "duration_s": 0,
        "severity": "critical",
        "cooldown_s": 60,
        "enabled": True,
    },
    {
        "target_name": "pve-host-01",
        "metric_name": "cpu_pct",
        "comparator": "gt",
        "threshold": 85.0,
        "duration_s": 120,
        "severity": "warning",
        "cooldown_s": 900,
        "enabled": True,
    },
    {
        "target_name": "pve-host-01",
        "metric_name": "mem_pct",
        "comparator": "gt",
        "threshold": 90.0,
        "duration_s": 120,
        "severity": "warning",
        "cooldown_s": 900,
        "enabled": True,
    },
]

def seed_rules(db):
    for r in SEED_RULES:
        target = db.query(Target).filter_by(name=r["target_name"]).first()
        if not target:
            print(f"Skipping rule — target not found: {r['target_name']}")
            continue
        exists = db.query(AlertRule).filter_by(
            target_id=target.id,
            metric_name=r["metric_name"],
            comparator=r["comparator"],
        ).first()
        if not exists:
            db.add(AlertRule(
                id=uuid.uuid4(),
                target_id=target.id,
                metric_name=r["metric_name"],
                comparator=r["comparator"],
                threshold=r["threshold"],
                duration_s=r["duration_s"],
                severity=r["severity"],
                cooldown_s=r["cooldown_s"],
                enabled=r["enabled"],
            ))
            print(f"Seeded rule: {r['metric_name']} {r['comparator']} {r['threshold']} on {r['target_name']}")
        else:
            print(f"Rule already exists, skipping: {r['metric_name']} on {r['target_name']}")
    db.commit()

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