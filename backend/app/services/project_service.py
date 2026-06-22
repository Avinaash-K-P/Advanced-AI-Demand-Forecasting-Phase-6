from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.user import User
from app.models.forecast_project import ForecastProject
from app.models.project_member import ProjectMember
from app.models.project_dataset import ProjectDataset
from app.models.project_forecast import ProjectForecast
from app.models.project_report import ProjectReport
from app.models.project_activity import ProjectActivity


# ──────────────────────────────────────────
# Activity Logger
# ──────────────────────────────────────────

def log_project_activity(
    db: Session,
    project_id: int,
    user_id: int,
    action: str,
    description: str = None
):
    activity = ProjectActivity(
        project_id=project_id,
        user_id=user_id,
        action=action,
        description=description
    )
    db.add(activity)
    db.commit()


# ──────────────────────────────────────────
# Permission Check
# ──────────────────────────────────────────

def check_project_access(
    db: Session,
    project_id: int,
    user_id: int,
    required_role: list = None
):
    project = db.query(ForecastProject).filter(
        ForecastProject.id == project_id
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Owner always has full access
    if project.owner_id == user_id:
        return project

    member = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == user_id
    ).first()

    if not member:
        raise HTTPException(status_code=403, detail="Access denied")

    if required_role and member.role not in required_role:
        raise HTTPException(
            status_code=403,
            detail=f"Requires one of roles: {required_role}"
        )

    return project


# ──────────────────────────────────────────
# Project CRUD
# ──────────────────────────────────────────

def create_project(db: Session, org_id: int, name: str, description: str, owner_id: int):

    project = ForecastProject(
        organization_id = org_id,
        name=name,
        description=description,
        owner_id=owner_id,
        status="active"
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    # Auto-add owner as member
    member = ProjectMember(
        project_id=project.id,
        user_id=owner_id,
        role="owner"
    )
    db.add(member)
    db.commit()

    log_project_activity(
        db=db,
        project_id=project.id,
        user_id=owner_id,
        action="PROJECT_CREATED",
        description=f"Project '{name}' created"
    )

    return project


def get_all_projects(db: Session, user_id: int):

    owned = db.query(ForecastProject).filter(
        ForecastProject.owner_id == user_id
    ).all()

    member_project_ids = db.query(ProjectMember.project_id).filter(
        ProjectMember.user_id == user_id
    ).all()

    member_ids = [m[0] for m in member_project_ids]

    member_projects = db.query(ForecastProject).filter(
        ForecastProject.id.in_(member_ids),
        ForecastProject.owner_id != user_id
    ).all()

    return owned + member_projects


def get_project_by_id(db: Session, project_id: int, user_id: int):
    return check_project_access(db, project_id, user_id)


def update_project(
    db: Session,
    project_id: int,
    user_id: int,
    name: str = None,
    description: str = None,
    status: str = None
):
    project = check_project_access(
        db, project_id, user_id,
        required_role=["owner", "editor"]
    )

    if name:
        project.name = name
    if description:
        project.description = description
    if status:
        project.status = status

    project.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(project)

    log_project_activity(
        db=db,
        project_id=project_id,
        user_id=user_id,
        action="PROJECT_UPDATED",
        description=f"Project '{project.name}' updated"
    )

    return project


def delete_project(db: Session, project_id: int, user_id: int):

    project = check_project_access(
        db, project_id, user_id,
        required_role=["owner"]
    )

    project.status = "archived"
    project.updated_at = datetime.utcnow()

    db.commit()

    log_project_activity(
        db=db,
        project_id=project_id,
        user_id=user_id,
        action="PROJECT_ARCHIVED",
        description=f"Project '{project.name}' archived"
    )

    return project


# ──────────────────────────────────────────
# Member Management
# ──────────────────────────────────────────

def add_member(db: Session, project_id: int, user_id: int, target_user_id: int, role: str):

    check_project_access(
        db, project_id, user_id,
        required_role=["owner"]
    )

    existing = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == target_user_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="User is already a member")

    member = ProjectMember(
        project_id=project_id,
        user_id=target_user_id,
        role=role
    )

    db.add(member)
    db.commit()
    db.refresh(member)

    log_project_activity(
        db=db,
        project_id=project_id,
        user_id=user_id,
        action="MEMBER_ADDED",
        description=f"User {target_user_id} added as {role}"
    )

    return member


def get_members(db: Session, project_id: int, user_id: int):
    check_project_access(db, project_id, user_id)
    return db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id
    ).all()


def update_member_role(
    db: Session,
    project_id: int,
    user_id: int,
    target_user_id: int,
    role: str
):
    check_project_access(
        db, project_id, user_id,
        required_role=["owner"]
    )

    member = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == target_user_id
    ).first()

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    member.role = role
    db.commit()
    db.refresh(member)

    log_project_activity(
        db=db,
        project_id=project_id,
        user_id=user_id,
        action="MEMBER_ROLE_UPDATED",
        description=f"User {target_user_id} role updated to {role}"
    )

    return member


def remove_member(db: Session, project_id: int, user_id: int, target_user_id: int):

    check_project_access(
        db, project_id, user_id,
        required_role=["owner"]
    )

    member = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == target_user_id
    ).first()

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    db.delete(member)
    db.commit()

    log_project_activity(
        db=db,
        project_id=project_id,
        user_id=user_id,
        action="MEMBER_REMOVED",
        description=f"User {target_user_id} removed from project"
    )


# ──────────────────────────────────────────
# Dataset / Forecast / Report Linking
# ──────────────────────────────────────────

def link_dataset(db: Session, project_id: int, user_id: int, dataset_name: str, sales_reference_id: int, username: str):

    check_project_access(
        db, project_id, user_id,
        required_role=["owner", "editor"]
    )

    dataset = ProjectDataset(
        project_id=project_id,
        dataset_name=dataset_name,
        sales_reference_id=sales_reference_id,
        uploaded_by=username
    )

    db.add(dataset)
    db.commit()
    db.refresh(dataset)

    log_project_activity(
        db=db,
        project_id=project_id,
        user_id=user_id,
        action="DATASET_LINKED",
        description=f"Dataset '{dataset_name}' linked to project"
    )

    return dataset


def link_forecast(db: Session, project_id: int, user_id: int, forecast_result_id: int, username: str):

    check_project_access(
        db, project_id, user_id,
        required_role=["owner", "editor"]
    )

    forecast = ProjectForecast(
        project_id=project_id,
        forecast_result_id=forecast_result_id,
        created_by=username
    )

    db.add(forecast)
    db.commit()
    db.refresh(forecast)

    log_project_activity(
        db=db,
        project_id=project_id,
        user_id=user_id,
        action="FORECAST_LINKED",
        description=f"Forecast result {forecast_result_id} linked to project"
    )

    return forecast


def link_report(db: Session, project_id: int, user_id: int, report_id: int, username: str):

    check_project_access(
        db, project_id, user_id,
        required_role=["owner", "editor"]
    )

    report = ProjectReport(
        project_id=project_id,
        report_id=report_id,
        added_by=username
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    log_project_activity(
        db=db,
        project_id=project_id,
        user_id=user_id,
        action="REPORT_LINKED",
        description=f"Report {report_id} linked to project"
    )

    return report


# ──────────────────────────────────────────
# Activity Feed
# ──────────────────────────────────────────

def get_project_activity(db: Session, project_id: int, user_id: int):
    check_project_access(db, project_id, user_id)
    return db.query(ProjectActivity).filter(
        ProjectActivity.project_id == project_id
    ).order_by(ProjectActivity.timestamp.desc()).all()