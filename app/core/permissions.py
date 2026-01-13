from fastapi import HTTPException, status

def require_role(membership, allowed_roles: set[str]) -> None:
    if membership.role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )

