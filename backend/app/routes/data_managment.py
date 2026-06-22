from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.db.database import get_db
from app.models.user import User
from app.core.security import get_current_user, verify_role
from app.utils.response import success_response
from app.services.dataset_service import (
    get_all_versions,
    get_version_by_id,
    get_upload_history,
    get_modifications,
    archive_dataset_version,
    restore_dataset_version,
    compare_dataset_versions
)

router = APIRouter(prefix="/datasets", tags=["Data Management"])


# ──────────────────────────────────────────
# 6.1 — Dataset Versions
# ──────────────────────────────────────────

@router.get("/versions")
def list_versions(
    dataset_name: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    user = Depends(verify_role("all"))
):
    versions = get_all_versions(db, dataset_name)
    return success_response(
        message="Dataset versions fetched successfully!",
        data=[{
            "id": v.id,
            "version_number": v.version_number,
            "dataset_name": v.dataset_name,
            "file_type": v.file_type,
            "total_rows": v.total_rows,
            "total_columns": v.total_columns,
            "file_size_kb": v.file_size_kb,
            "status": v.status,
            "is_archived": v.is_archived,
            "uploaded_by": v.uploaded_by,
            "uploaded_at": v.uploaded_at
        } for v in versions]
    )


@router.get("/versions/{version_id}")
def get_version(
    version_id: int,
    db: Session = Depends(get_db),
    user = Depends(verify_role("all"))
):
    v = get_version_by_id(db, version_id)
    return success_response(
        message="Dataset version fetched successfully!",
        data={
            "id": v.id,
            "version_number": v.version_number,
            "dataset_name": v.dataset_name,
            "file_type": v.file_type,
            "total_rows": v.total_rows,
            "total_columns": v.total_columns,
            "file_size_kb": v.file_size_kb,
            "columns_snapshot": v.columns_snapshot,
            "status": v.status,
            "is_archived": v.is_archived,
            "archived_at": v.archived_at,
            "uploaded_by": v.uploaded_by,
            "project_id": v.project_id,
            "uploaded_at": v.uploaded_at
        }
    )


# ──────────────────────────────────────────
# 6.2 — Upload History
# ──────────────────────────────────────────

@router.get("/upload-history")
def list_upload_history(
    dataset_name: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    user = Depends(verify_role("all"))
):
    history = get_upload_history(db, dataset_name=dataset_name)
    return success_response(
        message="Upload history fetched successfully!",
        data=[{
            "id": h.id,
            "dataset_version_id": h.dataset_version_id,
            "dataset_name": h.dataset_name,
            "uploaded_by": h.uploaded_by,
            "upload_status": h.upload_status,
            "rows_uploaded": h.rows_uploaded,
            "rows_cleaned": h.rows_cleaned,
            "duplicates_removed": h.duplicates_removed,
            "error_message": h.error_message,
            "uploaded_at": h.uploaded_at
        } for h in history]
    )


@router.get("/my-uploads")
def my_upload_history(
    db: Session = Depends(get_db),
    user = Depends(verify_role("all"))
):
    history = get_upload_history(db, uploaded_by=current_user.id)
    return success_response(
        message="Your upload history fetched successfully!",
        data=[{
            "id": h.id,
            "dataset_name": h.dataset_name,
            "upload_status": h.upload_status,
            "rows_uploaded": h.rows_uploaded,
            "rows_cleaned": h.rows_cleaned,
            "duplicates_removed": h.duplicates_removed,
            "uploaded_at": h.uploaded_at
        } for h in history]
    )


# ──────────────────────────────────────────
# 6.3 — Modification Tracking
# ──────────────────────────────────────────

@router.get("/versions/{version_id}/modifications")
def list_modifications(
    version_id: int,
    db: Session = Depends(get_db),
    user = Depends(verify_role("all"))
):
    mods = get_modifications(db, version_id)
    return success_response(
        message="Modifications fetched successfully!",
        data=[{
            "id": m.id,
            "modification_type": m.modification_type,
            "description": m.description,
            "rows_affected": m.rows_affected,
            "modified_by": m.modified_by,
            "modified_at": m.modified_at
        } for m in mods]
    )


# ──────────────────────────────────────────
# 6.4 — Archive / Restore
# ──────────────────────────────────────────

@router.put("/versions/{version_id}/archive")
def archive_version(
    version_id: int,
    db: Session = Depends(get_db),
    user = Depends(verify_role("analyst"))
):
    version = archive_dataset_version(db, version_id, current_user.id)
    return success_response(
        message="Dataset version archived successfully!",
        data={
            "id": version.id,
            "version_number": version.version_number,
            "status": version.status,
            "archived_at": version.archived_at
        }
    )


@router.put("/versions/{version_id}/restore")
def restore_version(
    version_id: int,
    db: Session = Depends(get_db),
    user = Depends(verify_role("analyst"))
):
    version = restore_dataset_version(db, version_id, current_user.id)
    return success_response(
        message="Dataset version restored successfully!",
        data={
            "id": version.id,
            "version_number": version.version_number,
            "status": version.status
        }
    )


# ──────────────────────────────────────────
# 6.5 — Dataset Comparison
# ──────────────────────────────────────────

@router.get("/compare")
def compare_versions(
    version_id_a: int = Query(..., description="First version ID"),
    version_id_b: int = Query(..., description="Second version ID"),
    db: Session = Depends(get_db),
    user = Depends(verify_role("all"))
):
    result = compare_dataset_versions(db, version_id_a, version_id_b)
    return success_response(
        message="Dataset comparison completed!",
        data=result
    )