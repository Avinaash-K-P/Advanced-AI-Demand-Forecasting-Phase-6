from fastapi import APIRouter, Depends
from app.core.security import verify_role

from app.schemas.kpi import (
    KPICreate,
    KPIValueCreate
)

from app.services.kpi_service import (
    create_kpi,
    get_all_kpis,
    create_kpi_value,
    get_kpi_trends,
    get_kpi_performance,
    generate_kpi_report,
    generate_kpi_alerts
)

router = APIRouter(
    prefix="/kpi",
    tags=["KPI Management"]
)

@router.post("/create")
def add_new_kpi(
    payload: KPICreate,
    user = Depends(verify_role("manager"))
):
    return create_kpi(payload)

@router.get("/")
def list_kpis(
    user = Depends(verify_role("all"))
):
    return get_all_kpis()

@router.post("/value")
def add_kpi_value(
    payload: KPIValueCreate,
    user = Depends(verify_role("manager"))
):
    return create_kpi_value(payload)

@router.get("/trends/{kpi_id}")
def kpi_trends(
    kpi_id: int,
    user = Depends(verify_role("all"))
):
    return get_kpi_trends(kpi_id)

@router.get("/performance/{kpi_id}")
def kpi_performance(
    kpi_id: int,
    user = Depends(verify_role("all"))    
):
    return get_kpi_performance(kpi_id) 

@router.get("/report/{kpi_id}")
def kpi_report(
    kpi_id: int,
    user = Depends(verify_role("all")) 
):
    return generate_kpi_report(kpi_id)

@router.post("/alerts/{kpi_id}")
def add_kpi_alert(
    kpi_id: int,
    user = Depends(verify_role("manager"))
):
    return generate_kpi_alerts(kpi_id)
        
                   