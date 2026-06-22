from fastapi import APIRouter, Depends

from app.core.security import verify_role

from app.schemas.notification import (
    NotificationCreate,
    NotificationPreferenceCreate,
    NotificationHistoryCreate
)

from app.services.notification_service import (
    create_notification,
    get_notifications,
    save_notification_preference,
    get_notification_preferences,
    create_notification_history,
    get_notification_history,
    get_role_notifications,
    get_organization_announcements
)

router = APIRouter(
    prefix="/notifications",
    tags=["Notification Center"]
)

@router.post("/")
def add_notification(
    payload: NotificationCreate,
    user=Depends(
        verify_role("admins")
    )
):
    return create_notification(payload)

@router.get("/{organization_id}")
def list_notifications(
    organization_id: int,
    user=Depends(
        verify_role("manager")
    )
):
    return get_notifications(
        organization_id
    )

@router.post("/preferences")
def save_preferences(
    payload: NotificationPreferenceCreate,
    user=Depends(
        verify_role("all")
    )
):
    return save_notification_preference(
        payload
    )

@router.get("/preferences/{user_id}")
def preferences(
    user_id: int,
    user=Depends(
        verify_role("all")
    )
):
    return get_notification_preferences(
        user_id
    )

@router.post("/history")
def add_history(
    payload: NotificationHistoryCreate,
    user=Depends(
        verify_role("admins")
    )
):
    return create_notification_history(
        payload
    )

@router.get("/history/{user_id}")
def history(
    user_id: int,
    user=Depends(
        verify_role("all")
    )
):
    return get_notification_history(
        user_id
    )

@router.get(
    "/role/{organization_id}/{role}"
)
def role_notifications(
    organization_id: int,
    role: str,
    user=Depends(
        verify_role("all")
    )
):
    return get_role_notifications(
        organization_id,
        role
    )                        

@router.get(
    "/announcements/{organization_id}"
)
def announcements(
    organization_id: int,
    user=Depends(
        verify_role("all")
    )
):
    return get_organization_announcements(
        organization_id
    )    