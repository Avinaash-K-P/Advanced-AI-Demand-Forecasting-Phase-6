from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.models.forecast_comments import ForecastComment
from app.core.security import get_current_user, verify_role
from app.utils.response import success_response
from app.schemas.forecast_comments import CommentCreate, CommentUpdate

router = APIRouter(prefix="/forecasts", tags=["Forecast Comments"])


# ── Add Comment ──
@router.post("/{forecast_id}/comments")
def add_comment(
    forecast_id: int,
    payload: CommentCreate,
    db: Session = Depends(get_db),
    user = Depends(verify_role("analyst"))
):
    comment = ForecastComment(
        forecast_id=forecast_id,
        user_id=current_user.id,
        comment=payload.comment
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)

    return success_response(
        message="Comment added successfully!",
        data={
            "id": comment.id,
            "forecast_id": comment.forecast_id,
            "user_id": comment.user_id,
            "comment": comment.comment,
            "created_at": comment.created_at
        }
    )


# ── Get Comments for a Forecast ──
@router.get("/{forecast_id}/comments")
def get_comments(
    forecast_id: int,
    db: Session = Depends(get_db),
    user = Depends(verify_role("all"))
):
    comments = db.query(ForecastComment).filter(
        ForecastComment.forecast_id == forecast_id
    ).order_by(ForecastComment.created_at.asc()).all()

    return success_response(
        message="Comments fetched successfully!",
        data=[{
            "id": c.id,
            "forecast_id": c.forecast_id,
            "user_id": c.user_id,
            "comment": c.comment,
            "created_at": c.created_at,
            "updated_at": c.updated_at
        } for c in comments]
    )


# ── Edit Comment ──
@router.put("/comments/{comment_id}")
def update_comment(
    comment_id: int,
    payload: CommentUpdate,
    db: Session = Depends(get_db),
    user = Depends(verify_role("team"))
):
    comment = db.query(ForecastComment).filter(
        ForecastComment.id == comment_id
    ).first()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only edit your own comments")

    comment.comment = payload.comment
    db.commit()
    db.refresh(comment)

    return success_response(
        message="Comment updated successfully!",
        data={
            "id": comment.id,
            "comment": comment.comment,
            "updated_at": comment.updated_at
        }
    )


# ── Delete Comment ──
@router.delete("/comments/{comment_id}")
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    user = Depends(verify_role("admins"))
):
    comment = db.query(ForecastComment).filter(
        ForecastComment.id == comment_id
    ).first()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only delete your own comments")

    db.delete(comment)
    db.commit()

    return success_response(message="Comment deleted successfully!")