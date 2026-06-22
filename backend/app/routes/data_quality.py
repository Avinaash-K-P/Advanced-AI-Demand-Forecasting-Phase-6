from fastapi import APIRouter, Depends
from app.core.security import verify_role

from app.schemas.data_quality import (
    DataQualityReportCreate,
    ValidationLogCreate
)

from app.services.data_quality_service import (
    generate_data_quality_report,
    create_validation_log,
    detect_incomplete_dataset,
    get_quality_report,
    get_validation_summary,
    get_quality_dashboard_metrics
)

router = APIRouter(
    prefix="/data-quality",
    tags=["Data Quality Management"]
)

@router.post("/report")
def create_quality_report(
    payload: DataQualityReportCreate,
    user = Depends(verify_role("analyst"))
):
    return generate_data_quality_report(
        organization_id=payload.organization_id,
        dataset_id=payload.dataset_id,
        generated_by=payload.generated_by
    )

@router.post("/validation-log")
def add_validation_log(
    payload: ValidationLogCreate,
    user = Depends(verify_role("analyst"))
):
    return create_validation_log(payload)    

@router.get("/detect/{organization_id}")
def detect_dataset_issues(
    organization_id: int,
    user = Depends(verify_role("analyst"))
):
    return detect_incomplete_dataset(
        organization_id
    )

@router.get("/report/{report_id}")
def view_quality_report(
    report_id: int,
    user = Depends(verify_role("manager"))
):
    return get_quality_report(
        report_id
    )

@router.get("/summary/{report_id}")
def validation_summary(
    report_id: int,
    user = Depends(verify_role("manager"))
):
    return get_validation_summary(
        report_id
    )            

@router.get("/dashboard/{organization_id}")
def dashboard_metrics(
    organization_id: int,
    user = Depends(verify_role("all"))
):
    return get_quality_dashboard_metrics(
        organization_id
    )    