from app.models.audit_log import AuditLog

class AuditLogService:
    def __init__(self, session):
        self.session = session

    def log(
        self,
        *,
        organization_id: int,
        actor_id: int | None,
        action: str,
        entity: str,
        entity_id: int | None = None,
        metadata: dict | None = None,
    ):
        log = AuditLog(
            organization_id=organization_id,
            actor_id=actor_id,
            action=action,
            entity=entity,
            entity_id=entity_id,
            metadata=metadata,
        )
        self.session.add(log)
