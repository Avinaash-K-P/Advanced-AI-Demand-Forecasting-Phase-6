from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.db.database import get_db
from app.models.user import User
from app.models.forecast_activity_timeline import ForecastActivityTimeline
from app.core.security import get_current_user, verify_role
from app.utils.response import success_response
from app.utils.timeline_logger import log_timeline_event, TimelineAction, TimelineCategory
from app.schemas.forecast_timeline import TimelineEventCreate

router = APIRouter(prefix="/timeline", tags=["Forecast Activity Timeline"])


# ── Get Full Timeline (with filters) ──
@router.get("/")
def get_timeline(
    forecast_id: Optional[int] = Query(None),
    project_id: Optional[int] = Query(None),
    category: Optional[str] = Query(None),
    action: Optional[str] = Query(None),
    limit: int = Query(50, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    user = Depends(verify_role("all"))
):
    query = db.query(ForecastActivityTimeline)

    if forecast_id:
        query = query.filter(ForecastActivityTimeline.forecast_id == forecast_id)

    if project_id:
        query = query.filter(ForecastActivityTimeline.project_id == project_id)

    if category:
        query = query.filter(ForecastActivityTimeline.category == category)

    if action:
        query = query.filter(ForecastActivityTimeline.action == action)

    events = query.order_by(
        ForecastActivityTimeline.timestamp.desc()
    ).limit(limit).all()

    return success_response(
        message="Timeline fetched successfully!",
        data=[{
            "id": e.id,
            "forecast_id": e.forecast_id,
            "project_id": e.project_id,
            "user_id": e.user_id,
            "action": e.action,
            "category": e.category,
            "description": e.description,
            "meta_value": e.meta_value,
            "timestamp": e.timestamp
        } for e in events]
    )


# ── Get Timeline for a Specific Forecast ──
@router.get("/forecast/{forecast_id}")
def get_forecast_timeline(
    forecast_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    user = Depends(verify_role("all"))
):
    events = db.query(ForecastActivityTimeline).filter(
        ForecastActivityTimeline.forecast_id == forecast_id
    ).order_by(ForecastActivityTimeline.timestamp.desc()).all()

    return success_response(
        message="Forecast timeline fetched successfully!",
        data=[{
            "id": e.id,
            "user_id": e.user_id,
            "action": e.action,
            "category": e.category,
            "description": e.description,
            "meta_value": e.meta_value,
            "timestamp": e.timestamp
        } for e in events]
    )


# ── Get Timeline for a Specific Project ──
@router.get("/project/{project_id}")
def get_project_timeline(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    user = Depends(verify_role("all"))
):
    events = db.query(ForecastActivityTimeline).filter(
        ForecastActivityTimeline.project_id == project_id
    ).order_by(ForecastActivityTimeline.timestamp.desc()).all()

    return success_response(
        message="Project timeline fetched successfully!",
        data=[{
            "id": e.id,
            "forecast_id": e.forecast_id,
            "user_id": e.user_id,
            "action": e.action,
            "category": e.category,
            "description": e.description,
            "meta_value": e.meta_value,
            "timestamp": e.timestamp
        } for e in events]
    )


# ── Get My Personal Activity Timeline ──
@router.get("/my-activity")
def get_my_activity(
    limit: int = Query(30, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    user = Depends(verify_role("all"))
):
    events = db.query(ForecastActivityTimeline).filter(
        ForecastActivityTimeline.user_id == current_user.id
    ).order_by(ForecastActivityTimeline.timestamp.desc()).limit(limit).all()

    return success_response(
        message="Your activity timeline fetched successfully!",
        data=[{
            "id": e.id,
            "forecast_id": e.forecast_id,
            "project_id": e.project_id,
            "action": e.action,
            "category": e.category,
            "description": e.description,
            "meta_value": e.meta_value,
            "timestamp": e.timestamp
        } for e in events]
    )


# ── Manual Log (Admin use) ──
@router.post("/log")
def manual_log(
    payload: TimelineEventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    user = Depends(verify_role("all"))
):
    log_timeline_event(
        db=db,
        user_id=current_user.id,
        action=payload.action,
        category=payload.category,
        forecast_id=payload.forecast_id,
        project_id=payload.project_id,
        description=payload.description,
        meta_value=payload.meta_value
    )

    return success_response(message="Timeline event logged successfully!")