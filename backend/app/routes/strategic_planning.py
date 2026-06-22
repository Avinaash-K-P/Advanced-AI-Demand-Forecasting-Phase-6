from fastapi import APIRouter, Depends
from app.core.security import verify_role

from app.schemas.strategic_planning import (
    AnnualPlanCreate,
    AnnualPlanUpdate,
    QuarterlyPlanCreate,
    QuarterlyPlanUpdate,
    BusinessTargetCreate,
    BusinessTargetUpdate
)

from app.services.strategic_planning_service import (
    create_annual_plan,
    update_annual_plan,
    create_quarterly_plan,
    update_quarterly_plan,
    create_business_target,
    update_business_target,
    get_annual_dashboard,
    get_quarterly_dashboard,
    compare_forecast_vs_target,
    generate_planning_recommendations
)

router = APIRouter(
    prefix="/planning",
    tags=["Strategic Planning"]
)

@router.post("/annual")
def add_annual(
    plan: AnnualPlanCreate,
    user = Depends(verify_role("manager"))
):
    return create_annual_plan(plan)


@router.put("/annual/{plan_id}")
def edit_annual(
    plan_id: int,
    plan: AnnualPlanUpdate,
    user = Depends(verify_role("manager"))
):
    return update_annual_plan(
        plan_id,
        plan
    )

@router.post("/quarterly")
def add_quarterly(
    plan: QuarterlyPlanCreate,
    user = Depends(verify_role("manager"))
):
    return create_quarterly_plan(plan)


@router.put("/quarterly/{plan_id}")
def edit_quarterly(
    plan_id: int,
    plan: QuarterlyPlanUpdate,
    user = Depends(verify_role("manager"))
):
    return update_quarterly_plan(
        plan_id,
        plan
    )

@router.post("/targets")
def add_target(
    target: BusinessTargetCreate,
    user = Depends(verify_role("manager"))
):
    return create_business_target(
        target
    )


@router.put("/targets/{target_id}")
def edit_target(
    target_id: int,
    target: BusinessTargetUpdate,
    user = Depends(verify_role("manager"))
):
    return update_business_target(
        target_id,
        target
    )

@router.get("/annual-dashboard/{org_id}")
def annual_dashboard(
    org_id: int,
    user = Depends(verify_role("manager"))
):
    return get_annual_dashboard(
        org_id
    )

@router.get("/quarterly-dashboard/{org_id}")
def quarterly_dashboard(
    org_id: int,
    user = Depends(verify_role("all"))
):
    return get_quarterly_dashboard(
        org_id
    )

@router.get("/forecast-vs-target/{org_id}")
def forecast_target_comparison(
    org_id: int,
    user = Depends(verify_role("all"))
):
    return compare_forecast_vs_target(
        org_id
    )

@router.get("/recommendations/{org_id}")
def planning_recommendations(
    org_id: int,
    user = Depends(verify_role("all"))
):
    return generate_planning_recommendations(
        org_id
    )