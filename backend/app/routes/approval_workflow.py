from fastapi import APIRouter, Depends
from app.core.security import verify_role

from app.schemas.forecast_approval import (
    ForecastApprovalCreate,
    ForecastApprovalReview
)

from app.services.approval_service import (
    submit_forecast_for_approval,
    approve_forecast,
    reject_forecast,
    get_approval_history,
    get_pending_approvals
)

router = APIRouter(
    prefix="/approvals",
    tags=["Forecast Approval Workflow"]
)


@router.post("/submit")
def submit_forecast(
    approval_data: ForecastApprovalCreate,
    user = Depends(verify_role("analyst"))
):
    return submit_forecast_for_approval(
        approval_data
    )


@router.post("/{approval_id}/approve")
def approve(
    approval_id: int,
    review_data: ForecastApprovalReview,
    user = Depends(verify_role("manager"))
):
    return approve_forecast(
        approval_id,
        review_data
    )


@router.post("/{approval_id}/reject")
def reject(
    approval_id: int,
    review_data: ForecastApprovalReview,
    user = Depends(verify_role("manager"))
):
    return reject_forecast(
        approval_id,
        review_data
    )


@router.get("/history/{forecast_id}")
def approval_history(
    forecast_id: int,
    user = Depends(verify_role("all"))
):
    return get_approval_history(
        forecast_id
    )


@router.get("/pending")
def pending_approvals(
    user = Depends(verify_role("all"))
):
    return get_pending_approvals()