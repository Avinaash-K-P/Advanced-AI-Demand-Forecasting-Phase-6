from fastapi import APIRouter, Depends
from app.core.security import verify_role

from app.schemas.governance import (
    ForecastLifecycleUpdate
)

from app.services.governance_service import (
    get_forecast_versions,
    get_forecast_activity_timeline,
    get_governance_audit_logs,
    update_forecast_lifecycle,
    get_governance_dashboard
)

router = APIRouter(
    prefix="/governance",
    tags=["Forecast Governance"]
)

@router.get("/versions/{forecast_date}")
def forecast_versions(
    forecast_date: str,
    user = Depends(verify_role("team"))
):
    return get_forecast_versions(
        forecast_date
    )

@router.get("/activity-timeline")
def activity_timeline(
    user = Depends(verify_role("team"))
):
    return get_forecast_activity_timeline()

@router.get("/audit-logs")
def governance_audit(
    user = Depends(verify_role("team"))
):
    return get_governance_audit_logs()

@router.get("/lifecycle")
def forecast_lifecycle(
    lifecycle_data: ForecastLifecycleUpdate,
    user = Depends(verify_role("team"))
):
    return update_forecast_lifecycle(lifecycle_data)

@router.get("/dashboard")
def governance_dashboard(
    user = Depends(verify_role("team"))
):
    return get_governance_dashboard()