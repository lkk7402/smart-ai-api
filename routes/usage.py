from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import User, UsageLog
from schemas import UsageStatsResponse, EndpointUsage
from auth.utils import get_current_user

router = APIRouter(prefix="/usage", tags=["usage"])


@router.get("", response_model=UsageStatsResponse)
def get_usage(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    rows = (
        db.query(UsageLog.endpoint, func.count(UsageLog.id).label("count"))
        .filter(UsageLog.user_id == current_user.id)
        .group_by(UsageLog.endpoint)
        .all()
    )
    breakdown = [EndpointUsage(endpoint=r.endpoint, count=r.count) for r in rows]
    total = sum(e.count for e in breakdown)
    return UsageStatsResponse(total=total, breakdown=breakdown)
