from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.db.database import get_db
from app.models.user import User
from app.models.forecast_revision import ForecastRevision
from app.core.security import get_current_user, verify_role
from app.utils.response import success_response
from app.services.revision_service import (
    snapshot_forecast_revision,
    get_revisions_by_date,
    get_latest_revision,
    compare_revisions
)

router = APIRouter(prefix="/revisions", tags=["Forecast Revisions"])


# ── Get All Revisions for a Forecast Date ──
@router.get("/")
def get_revisions(
    forecast_date: str = Query(..., description="Format: YYYY-MM-DD"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    user = Depends(verify_role("all"))
):
    revisions = get_revisions_by_date(db, forecast_date)

    if not revisions:
        raise HTTPException(
            status_code=404,
            detail=f"No revisions found for date {forecast_date}"
        )

    return success_response(
        message="Revisions fetched successfully!",
        data=[{
            "id": r.id,
            "revision_number": r.revision_number,
            "forecast_date": r.forecast_date,
            "predicted_demand": r.predicted_demand,
            "confidence_score": r.confidence_score,
            "model_type": r.model_type,
            "change_summary": r.change_summary,
            "created_by": r.created_by,
            "created_at": r.created_at
        } for r in revisions]
    )


# ── Get Latest Revision for a Forecast Date ──
@router.get("/latest")
def get_latest(
    forecast_date: str = Query(..., description="Format: YYYY-MM-DD"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    user = Depends(verify_role("all"))
):
    revision = get_latest_revision(db, forecast_date)

    if not revision:
        raise HTTPException(
            status_code=404,
            detail=f"No revisions found for date {forecast_date}"
        )

    return success_response(
        message="Latest revision fetched successfully!",
        data={
            "id": revision.id,
            "revision_number": revision.revision_number,
            "forecast_date": revision.forecast_date,
            "predicted_demand": revision.predicted_demand,
            "prophet_prediction": revision.prophet_prediction,
            "lr_prediction": revision.lr_prediction,
            "ma_prediction": revision.ma_prediction,
            "confidence_score": revision.confidence_score,
            "sales_trend": revision.sales_trend,
            "change_summary": revision.change_summary,
            "created_at": revision.created_at
        }
    )


# ── Compare Two Revisions ──
@router.get("/compare")
def compare(
    forecast_date: str = Query(..., description="Format: YYYY-MM-DD"),
    revision_a: int = Query(..., description="First revision number"),
    revision_b: int = Query(..., description="Second revision number"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    user = Depends(verify_role("all"))
    
):
    if revision_a == revision_b:
        raise HTTPException(
            status_code=400,
            detail="revision_a and revision_b must be different"
        )

    result = compare_revisions(db, forecast_date, revision_a, revision_b)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="One or both revisions not found for the given date"
        )

    return success_response(
        message="Revision comparison completed!",
        data=result
    )


# ── Get Full Detail of a Single Revision ──
@router.get("/{revision_id}")
def get_revision_detail(
    revision_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    user = Depends(verify_role("all"))
):
    revision = db.query(ForecastRevision).filter(
        ForecastRevision.id == revision_id
    ).first()

    if not revision:
        raise HTTPException(status_code=404, detail="Revision not found")

    return success_response(
        message="Revision detail fetched successfully!",
        data={
            "id": revision.id,
            "revision_number": revision.revision_number,
            "forecast_date": revision.forecast_date,
            "predicted_demand": revision.predicted_demand,
            "prophet_prediction": revision.prophet_prediction,
            "lr_prediction": revision.lr_prediction,
            "ma_prediction": revision.ma_prediction,
            "sales_trend": revision.sales_trend,
            "weekly_pattern": revision.weekly_pattern,
            "yearly_pattern": revision.yearly_pattern,
            "confidence_score": revision.confidence_score,
            "model_type": revision.model_type,
            "change_summary": revision.change_summary,
            "created_by": revision.created_by,
            "project_id": revision.project_id,
            "created_at": revision.created_at
        }
    )


# ── Manual Snapshot (Admin / Testing) ──
@router.post("/snapshot")
def manual_snapshot(
    project_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    user = Depends(verify_role("all"))
):
    snapshot_forecast_revision(
        db=db,
        user_id=current_user.id,
        project_id=project_id
    )

    return success_response(
        message="Forecast revision snapshot saved successfully!"
    )