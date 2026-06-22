from fastapi import APIRouter, Depends
from app.core.security import get_current_user, verify_role
from app.schemas.executive import ExecutiveAlertCreate

from app.services.executive_service import (
    get_executive_dashboard,
    get_forecast_metrics,
    get_planning_insights,
    get_business_summary,
    create_executive_alert,
    get_executive_alerts
)

from app.core.security import verify_role

router = APIRouter(
    prefix="/executive",
    tags=["Executive Command Center"]
)

@router.get("/dashboard/{organization_id}")
def executive_dashboard(
    organization_id: int,
    user=Depends(
        verify_role("manager")
    )
):
    return get_executive_dashboard(
        organization_id
    )

@router.get("/forecast-metrics/{organization_id}")
def forecast_metrics(
    organization_id: int,
    user=Depends(
        verify_role("manager")
    )
):
    return get_forecast_metrics(
        organization_id
    )

@router.get("/planning-insights/{organization_id}")
def planning_insights(
    organization_id: int,
    user=Depends(
        verify_role("manager")
    )
):
    return get_planning_insights(
        organization_id
    )

@router.get("/business-summary/{organization_id}")
def business_summary(
    organization_id: int,
    user=Depends(
        verify_role("manager")
    )
):
    return get_business_summary(
        organization_id
    )

@router.post("/alerts")
def add_executive_alert(
    payload: ExecutiveAlertCreate,
    user=Depends(
        verify_role("admins")
    )
):
    return create_executive_alert(
        payload
    )

@router.get("/alerts/{organization_id}")
def executive_alerts(
    organization_id: int,
    user=Depends(
        verify_role("manager")
    )
):
    return get_executive_alerts(
        organization_id
    )        
