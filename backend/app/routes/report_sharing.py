from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.database import get_db
from app.models.user import User
from app.models.report_sharing import ReportShare
from app.models.reports import Report
from app.core.security import get_current_user, verify_role
from app.utils.response import success_response
from app.schemas.report_sharing import ReportShareCreate

router = APIRouter(prefix="/reports", tags=["Report Sharing"])


# ── Share a Report ──
@router.post("/{report_id}/share")
def share_report(
    report_id: int,
    payload: ReportShareCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    user = Depends(verify_role("team"))
):
    # Check report exists
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    # Prevent sharing to yourself
    if payload.shared_to == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot share a report with yourself")

    # Prevent duplicate active share
    existing = db.query(ReportShare).filter(
        ReportShare.report_id == report_id,
        ReportShare.shared_to == payload.shared_to,
        ReportShare.is_active == True
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Report already shared with this user")

    share = ReportShare(
        report_id=report_id,
        shared_by=current_user.id,
        shared_to=payload.shared_to,
        permission=payload.permission,
        expires_at=payload.expires_at
    )

    db.add(share)
    db.commit()
    db.refresh(share)

    return success_response(
        message="Report shared successfully!",
        data={
            "id": share.id,
            "report_id": share.report_id,
            "shared_to": share.shared_to,
            "permission": share.permission,
            "expires_at": share.expires_at,
            "shared_at": share.shared_at
        }
    )


# ── Get All Shares for a Report ──
@router.get("/{report_id}/shares")
def get_report_shares(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    user = Depends(verify_role("all"))
):
    shares = db.query(ReportShare).filter(
        ReportShare.report_id == report_id,
        ReportShare.is_active == True
    ).all()

    return success_response(
        message="Report shares fetched successfully!",
        data=[{
            "id": s.id,
            "shared_to": s.shared_to,
            "permission": s.permission,
            "shared_at": s.shared_at,
            "expires_at": s.expires_at
        } for s in shares]
    )


# ── Get Reports Shared With Me ──
@router.get("/shared-with-me")
def get_shared_with_me(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    user = Depends(verify_role("all"))
):
    now = datetime.utcnow()

    shares = db.query(ReportShare).filter(
        ReportShare.shared_to == current_user.id,
        ReportShare.is_active == True
    ).all()

    # Filter out expired shares
    active_shares = [
        s for s in shares
        if s.expires_at is None or s.expires_at > now
    ]

    return success_response(
        message="Shared reports fetched successfully!",
        data=[{
            "id": s.id,
            "report_id": s.report_id,
            "shared_by": s.shared_by,
            "permission": s.permission,
            "shared_at": s.shared_at,
            "expires_at": s.expires_at
        } for s in active_shares]
    )


# ── Revoke a Share ──
@router.delete("/shares/{share_id}/revoke")
def revoke_share(
    share_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    user = Depends(verify_role("team"))
):
    share = db.query(ReportShare).filter(
        ReportShare.id == share_id
    ).first()

    if not share:
        raise HTTPException(status_code=404, detail="Share not found")

    if share.shared_by != current_user.id:
        raise HTTPException(status_code=403, detail="Only the person who shared can revoke access")

    share.is_active = False
    db.commit()

    return success_response(message="Report share revoked successfully!")