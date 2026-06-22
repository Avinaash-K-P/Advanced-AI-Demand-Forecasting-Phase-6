from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.database import get_db
from app.models.user import User
from app.models.project_collaboration import CollaborationInvitation
from app.models.project_discussion import ProjectDiscussion
from app.models.project_member import ProjectMember
from app.models.project_activity import ProjectActivity
from app.core.security import get_current_user, verify_role
from app.utils.response import success_response
from app.schemas.collaboration import (
    InvitationCreate,
    InvitationRespond,
    DiscussionCreate,
    DiscussionUpdate
)

router = APIRouter(prefix="/collaboration", tags=["Collaboration"])


# ── Helper: Check project membership ──
def get_member(db, project_id, user_id):
    return db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == user_id
    ).first()


# ── Helper: Log project activity ──
def log_activity(db, project_id, user_id, action, description=None):
    activity = ProjectActivity(
        project_id=project_id,
        user_id=user_id,
        action=action,
        description=description
    )
    db.add(activity)
    db.commit()


# ──────────────────────────────────────────
# Invitations
# ──────────────────────────────────────────

# Send Invitation
@router.post("/projects/{project_id}/invite")
def send_invitation(
    project_id: int,
    payload: InvitationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    user = Depends(verify_role("manager"))
):
    # Only owner can invite
    member = get_member(db, project_id, current_user.id)
    if not member or member.role != "owner":
        raise HTTPException(status_code=403, detail="Only the project owner can send invitations")

    # Prevent self-invite
    if payload.invited_user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot invite yourself")

    # Check if already a member
    already_member = get_member(db, project_id, payload.invited_user_id)
    if already_member:
        raise HTTPException(status_code=400, detail="User is already a member of this project")

    # Check for existing pending invitation
    existing = db.query(CollaborationInvitation).filter(
        CollaborationInvitation.project_id == project_id,
        CollaborationInvitation.invited_user_id == payload.invited_user_id,
        CollaborationInvitation.status == "pending"
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="A pending invitation already exists for this user")

    invitation = CollaborationInvitation(
        project_id=project_id,
        invited_by=current_user.id,
        invited_user_id=payload.invited_user_id,
        role=payload.role,
        message=payload.message
    )

    db.add(invitation)
    db.commit()
    db.refresh(invitation)

    log_activity(
        db=db,
        project_id=project_id,
        user_id=current_user.id,
        action="INVITATION_SENT",
        description=f"User {payload.invited_user_id} invited as {payload.role}"
    )

    return success_response(
        message="Invitation sent successfully!",
        data={
            "id": invitation.id,
            "project_id": invitation.project_id,
            "invited_user_id": invitation.invited_user_id,
            "role": invitation.role,
            "status": invitation.status,
            "invited_at": invitation.invited_at
        }
    )


# My Pending Invitations
@router.get("/my-invitations")
def get_my_invitations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    user = Depends(verify_role("all"))
):
    invitations = db.query(CollaborationInvitation).filter(
        CollaborationInvitation.invited_user_id == current_user.id,
        CollaborationInvitation.status == "pending"
    ).all()

    return success_response(
        message="Pending invitations fetched successfully!",
        data=[{
            "id": i.id,
            "project_id": i.project_id,
            "invited_by": i.invited_by,
            "role": i.role,
            "message": i.message,
            "invited_at": i.invited_at
        } for i in invitations]
    )


# Respond to Invitation (accept / decline)
@router.put("/invitations/{invitation_id}/respond")
def respond_to_invitation(
    invitation_id: int,
    payload: InvitationRespond,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    user = Depends(verify_role("all"))
):
    if payload.status not in ["accepted", "declined"]:
        raise HTTPException(status_code=400, detail="Status must be 'accepted' or 'declined'")

    invitation = db.query(CollaborationInvitation).filter(
        CollaborationInvitation.id == invitation_id,
        CollaborationInvitation.invited_user_id == current_user.id
    ).first()

    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found")

    if invitation.status != "pending":
        raise HTTPException(status_code=400, detail="Invitation has already been responded to")

    invitation.status = payload.status
    invitation.responded_at = datetime.utcnow()
    db.commit()

    # If accepted — auto add as project member
    if payload.status == "accepted":
        new_member = ProjectMember(
            project_id=invitation.project_id,
            user_id=current_user.id,
            role=invitation.role
        )
        db.add(new_member)
        db.commit()

        log_activity(
            db=db,
            project_id=invitation.project_id,
            user_id=current_user.id,
            action="INVITATION_ACCEPTED",
            description=f"User {current_user.id} joined as {invitation.role}"
        )

    else:
        log_activity(
            db=db,
            project_id=invitation.project_id,
            user_id=current_user.id,
            action="INVITATION_DECLINED",
            description=f"User {current_user.id} declined the invitation"
        )

    return success_response(
        message=f"Invitation {payload.status} successfully!",
        data={
            "invitation_id": invitation.id,
            "status": invitation.status,
            "responded_at": invitation.responded_at
        }
    )


# Get All Invitations for a Project
@router.get("/projects/{project_id}/invitations")
def get_project_invitations(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    user = Depends(verify_role("manager"))
):
    member = get_member(db, project_id, current_user.id)
    if not member:
        raise HTTPException(status_code=403, detail="Access denied")

    invitations = db.query(CollaborationInvitation).filter(
        CollaborationInvitation.project_id == project_id
    ).order_by(CollaborationInvitation.invited_at.desc()).all()

    return success_response(
        message="Project invitations fetched successfully!",
        data=[{
            "id": i.id,
            "invited_user_id": i.invited_user_id,
            "role": i.role,
            "status": i.status,
            "message": i.message,
            "invited_at": i.invited_at,
            "responded_at": i.responded_at
        } for i in invitations]
    )


# ──────────────────────────────────────────
# Project Discussions
# ──────────────────────────────────────────

# Post a Message
@router.post("/projects/{project_id}/discussions")
def post_discussion(
    project_id: int,
    payload: DiscussionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    user = Depends(verify_role("analyst"))
):
    member = get_member(db, project_id, current_user.id)
    if not member:
        raise HTTPException(status_code=403, detail="You are not a member of this project")

    discussion = ProjectDiscussion(
        project_id=project_id,
        user_id=current_user.id,
        message=payload.message,
        parent_id=payload.parent_id
    )

    db.add(discussion)
    db.commit()
    db.refresh(discussion)

    log_activity(
        db=db,
        project_id=project_id,
        user_id=current_user.id,
        action="DISCUSSION_POSTED",
        description=f"New {'reply' if payload.parent_id else 'message'} posted in project discussion"
    )

    return success_response(
        message="Discussion posted successfully!",
        data={
            "id": discussion.id,
            "project_id": discussion.project_id,
            "user_id": discussion.user_id,
            "message": discussion.message,
            "parent_id": discussion.parent_id,
            "created_at": discussion.created_at
        }
    )


# Get All Discussions for a Project
@router.get("/projects/{project_id}/discussions")
def get_discussions(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    user = Depends(verify_role("all"))
):
    member = get_member(db, project_id, current_user.id)
    if not member:
        raise HTTPException(status_code=403, detail="You are not a member of this project")

    # Fetch only top-level messages (replies attached via parent_id)
    discussions = db.query(ProjectDiscussion).filter(
        ProjectDiscussion.project_id == project_id,
        ProjectDiscussion.parent_id == None
    ).order_by(ProjectDiscussion.created_at.asc()).all()

    def format_discussion(d):
        return {
            "id": d.id,
            "user_id": d.user_id,
            "message": d.message,
            "created_at": d.created_at,
            "updated_at": d.updated_at,
            "replies": [format_discussion(r) for r in d.replies]
        }

    return success_response(
        message="Discussions fetched successfully!",
        data=[format_discussion(d) for d in discussions]
    )


# Edit a Discussion Message
@router.put("/discussions/{discussion_id}")
def update_discussion(
    discussion_id: int,
    payload: DiscussionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    user = Depends(verify_role("analyst"))
):
    discussion = db.query(ProjectDiscussion).filter(
        ProjectDiscussion.id == discussion_id
    ).first()

    if not discussion:
        raise HTTPException(status_code=404, detail="Discussion not found")

    if discussion.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only edit your own messages")

    discussion.message = payload.message
    db.commit()
    db.refresh(discussion)

    return success_response(
        message="Discussion updated successfully!",
        data={
            "id": discussion.id,
            "message": discussion.message,
            "updated_at": discussion.updated_at
        }
    )


# Delete a Discussion Message
@router.delete("/discussions/{discussion_id}")
def delete_discussion(
    discussion_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    user = Depends(verify_role("manager"))
):
    discussion = db.query(ProjectDiscussion).filter(
        ProjectDiscussion.id == discussion_id
    ).first()

    if not discussion:
        raise HTTPException(status_code=404, detail="Discussion not found")

    if discussion.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only delete your own messages")

    db.delete(discussion)
    db.commit()

    return success_response(message="Discussion deleted successfully!")