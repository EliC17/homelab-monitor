from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.alert import AlertRule, AlertEvent
from app.models.metric import MetricSample
 
COMPARATORS = {
    "gt": lambda v, t: v > t, "lt": lambda v, t: v < t,
    "eq": lambda v, t: v == t, "neq": lambda v, t: v != t,
}
 
def evaluate_rule(db: Session, rule: AlertRule, sample: MetricSample):
    breached = COMPARATORS[rule.comparator](sample.value, rule.threshold)
    active_event = (db.query(AlertEvent)
        .filter_by(rule_id=rule.id, target_id=sample.target_id, resolved_at=None)
        .first())
 
    if breached and not active_event:
        # check duration_s: has it been breaching this long? (simplified —
        # query recent samples for this target/metric and confirm all breach)
        recent = (db.query(MetricSample)
            .filter(MetricSample.target_id == sample.target_id,
                    MetricSample.metric_name == rule.metric_name,
                    MetricSample.recorded_at >= datetime.utcnow() - timedelta(seconds=rule.duration_s))
            .all())
        if all(COMPARATORS[rule.comparator](r.value, rule.threshold) for r in recent):
            event = AlertEvent(rule_id=rule.id, target_id=sample.target_id, triggering_value=sample.value)
            db.add(event)
            db.commit()
            dispatch(db, rule, event)
 
    elif not breached and active_event:
        active_event.resolved_at = datetime.utcnow()
        db.commit()
