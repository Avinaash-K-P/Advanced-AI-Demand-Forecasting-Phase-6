from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.core.security import get_current_user, verify_role
from app.utils.response import success_response
from app.schemas.forecast_project import (
    ProjectCreate,
    ProjectUpdate,
    MemberAdd,
    MemberRoleUpdate,
    DatasetLink,
    ForecastLink,
    ReportLink,
)
from app.services import project_service

router = APIRouter(prefix="/projects", tags=["Forecast Projects"])


# ──────────────────────────────────────────
# Project CRUD
# ──────────────────────────────────────────

@router.post("/create")
def create_project(
    payload: ProjectCreate,
    db: Session = Depends(get_db),
    user = Depends(verify_role("analyst")),
    current_user: User = Depends(get_current_user)
):
    project = project_service.create_project(
        db=db,
        org_id = current_user.organization_id,
        name=payload.name,
        description=payload.description,
        owner_id=current_user.id
    )
    return success_response(
        message="Project created successfully!",
        data={"id": project.id, "name": project.name, "status": project.status}
    )


@router.get("/")
def list_projects(
    db: Session = Depends(get_db),
    user = Depends(verify_role("team")),
    current_user: User = Depends(get_current_user)
):
    projects = project_service.get_all_projects(
        db=db,
        user_id=current_user.id
    )
    return success_response(
        message="Projects fetched successfully!",
        data=[{
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "status": p.status,
            "owner_id": p.owner_id,
            "created_at": p.created_at
        } for p in projects]
    )


@router.get("/{project_id}")
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    user = Depends(verify_role("team")),
    current_user: User = Depends(get_current_user)
):
    project = project_service.get_project_by_id(
        db=db,
        project_id=project_id,
        user_id=current_user.id
    )
    return success_response(
        message="Project fetched successfully!",
        data={
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "status": project.status,
            "owner_id": project.owner_id,
            "created_at": project.created_at,
            "updated_at": project.updated_at
        }
    )


@router.put("/{project_id}/update")
def update_project(
    project_id: int,
    payload: ProjectUpdate,
    db: Session = Depends(get_db),
    user = Depends(verify_role("manager")),
    current_user: User = Depends(get_current_user)
):
    project = project_service.update_project(
        db=db,
        project_id=project_id,
        user_id=current_user.id,
        name=payload.name,
        description=payload.description,
        status=payload.status
    )
    return success_response(
        message="Project updated successfully!",
        data={"id": project.id, "name": project.name, "status": project.status}
    )


@router.delete("/{project_id}/delete")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    user = Depends(verify_role("admins")),
    current_user: User = Depends(get_current_user)
):
    project_service.delete_project(
        db=db,
        project_id=project_id,
        user_id=current_user.id
    )
    return success_response(message="Project archived successfully!")


# ──────────────────────────────────────────
# Member Management
# ──────────────────────────────────────────

@router.post("/{project_id}/members/add")
def add_member(
    project_id: int,
    payload: MemberAdd,
    db: Session = Depends(get_db),
    user = Depends(verify_role("admins")),
    current_user: User = Depends(get_current_user)
):
    member = project_service.add_member(
        db=db,
        project_id=project_id,
        user_id=current_user.id,
        target_user_id=payload.user_id,
        role=payload.role
    )
    return success_response(
        message="Member added successfully!",
        data={"user_id": member.user_id, "role": member.role}
    )


@router.get("/{project_id}/members")
def get_members(
    project_id: int,
    db: Session = Depends(get_db),
    user = Depends(verify_role("team")),
    current_user: User = Depends(get_current_user)
):
    members = project_service.get_members(
        db=db,
        project_id=project_id,
        user_id=current_user.id
    )
    return success_response(
        message="Members fetched successfully!",
        data=[{
            "id": m.id,
            "user_id": m.user_id,
            "role": m.role,
            "joined_at": m.joined_at
        } for m in members]
    )


@router.put("/{project_id}/members/{target_user_id}")
def update_member_role(
    project_id: int,
    target_user_id: int,
    payload: MemberRoleUpdate,
    db: Session = Depends(get_db),
    user = Depends(verify_role("manager")),
    current_user: User = Depends(get_current_user)
):
    member = project_service.update_member_role(
        db=db,
        project_id=project_id,
        user_id=current_user.id,
        target_user_id=target_user_id,
        role=payload.role
    )
    return success_response(
        message="Member role updated successfully!",
        data={"user_id": member.user_id, "role": member.role}
    )


@router.delete("/{project_id}/members/{target_user_id}")
def remove_member(
    project_id: int,
    target_user_id: int,
    db: Session = Depends(get_db),
    user = Depends(verify_role("admin")),
    current_user: User = Depends(get_current_user)
):
    project_service.remove_member(
        db=db,
        project_id=project_id,
        user_id=current_user.id,
        target_user_id=target_user_id
    )
    return success_response(message="Member removed successfully!")


# ──────────────────────────────────────────
# Dataset / Forecast / Report Linking
# ──────────────────────────────────────────

@router.post("/{project_id}/datasets/link")
def link_dataset(
    project_id: int,
    payload: DatasetLink,
    db: Session = Depends(get_db),
    user = Depends(verify_role("analyst")),
    current_user: User = Depends(get_current_user)
):
    dataset = project_service.link_dataset(
        db=db,
        project_id=project_id,
        user_id=current_user.id,
        dataset_name=payload.dataset_name,
        sales_reference_id=payload.sales_reference_id,
        username=current_user.username
    )
    return success_response(
        message="Dataset linked successfully!",
        data={"id": dataset.id, "dataset_name": dataset.dataset_name}
    )


@router.post("/{project_id}/forecasts/link")
def link_forecast(
    project_id: int,
    payload: ForecastLink,
    db: Session = Depends(get_db),
    user = Depends(verify_role("analyst")),
    current_user: User = Depends(get_current_user)
):
    forecast = project_service.link_forecast(
        db=db,
        project_id=project_id,
        user_id=current_user.id,
        forecast_result_id=payload.forecast_result_id,
        username=current_user.username
    )
    return success_response(
        message="Forecast linked successfully!",
        data={"id": forecast.id, "forecast_result_id": forecast.forecast_result_id}
    )


@router.post("/{project_id}/reports/link")
def link_report(
    project_id: int,
    payload: ReportLink,
    db: Session = Depends(get_db),
    user = Depends(verify_role("analyst")),
    current_user: User = Depends(get_current_user)
):
    report = project_service.link_report(
        db=db,
        project_id=project_id,
        user_id=current_user.id,
        report_id=payload.report_id,
        username=current_user.username
    )
    return success_response(
        message="Report linked successfully!",
        data={"id": report.id, "report_id": report.report_id}
    )


# ──────────────────────────────────────────
# Activity Feed
# ──────────────────────────────────────────

@router.get("/{project_id}/activity")
def get_activity(
    project_id: int,
    db: Session = Depends(get_db),
    user = Depends(verify_role("team")),
    current_user: User = Depends(get_current_user)
):
    activities = project_service.get_project_activity(
        db=db,
        project_id=project_id,
        user_id=current_user.id
    )
    return success_response(
        message="Activity fetched successfully!",
        data=[{
            "id": a.id,
            "user_id": a.user_id,
            "action": a.action,
            "description": a.description,
            "timestamp": a.timestamp
        } for a in activities]
    )