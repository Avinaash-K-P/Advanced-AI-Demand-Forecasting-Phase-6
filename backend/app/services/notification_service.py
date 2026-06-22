from datetime import datetime

from app.db.session import SessionLocal

from app.models.notification import Notifications
from app.models.notification_preference import NotificationPreferences
from app.models.notification_history import NotificationHistory

from app.schemas.notification import (
    NotificationCreate,
    NotificationPreferenceCreate,
    NotificationHistoryCreate
)

from app.utils.response import (
    success_response,
    error_response
)

def create_notification(
    payload: NotificationCreate
):

    db = SessionLocal()

    try:

        notification = Notifications(

            organization_id=payload.organization_id,

            title=payload.title,

            message=payload.message,

            notification_type=payload.notification_type,

            target_role=payload.target_role,

            status=payload.status,

            created_by=payload.created_by
        )

        db.add(notification)

        db.commit()

        db.refresh(notification)

        return success_response(
            message="Notification created successfully",
            data=notification
        )

    except Exception as e:

        db.rollback()

        return error_response(
            message="Failed to create notification",
            details=str(e)
        )

    finally:

        db.close()

def get_notifications(
    organization_id: int
):

    db = SessionLocal()

    try:

        notifications = db.query(
            Notifications
        ).filter(
            Notifications.organization_id == organization_id
        ).all()

        return success_response(
            message="Notifications retrieved successfully",
            data=notifications
        )

    finally:

        db.close()

def save_notification_preference(
    payload: NotificationPreferenceCreate
):

    db = SessionLocal()

    try:

        preference = db.query(
            NotificationPreferences
        ).filter(
            NotificationPreferences.user_id == payload.user_id
        ).first()

        if preference:

            preference.email_enabled = payload.email_enabled
            preference.in_app_enabled = payload.in_app_enabled
            preference.forecast_alerts = payload.forecast_alerts
            preference.workflow_alerts = payload.workflow_alerts
            preference.report_alerts = payload.report_alerts

        else:

            preference = NotificationPreferences(

                user_id=payload.user_id,

                email_enabled=payload.email_enabled,

                in_app_enabled=payload.in_app_enabled,

                forecast_alerts=payload.forecast_alerts,

                workflow_alerts=payload.workflow_alerts,

                report_alerts=payload.report_alerts
            )

            db.add(preference)

        db.commit()

        return success_response(
            message="Notification preferences saved"
        )

    except Exception as e:

        db.rollback()

        return error_response(
            message="Failed to save preferences",
            details=str(e)
        )

    finally:

        db.close()                

def get_notification_preferences(
    user_id: int
):

    db = SessionLocal()

    try:

        preferences = db.query(
            NotificationPreferences
        ).filter(
            NotificationPreferences.user_id == user_id
        ).first()

        return success_response(
            message="Preferences retrieved",
            data=preferences
        )

    finally:

        db.close()

def create_notification_history(
    payload: NotificationHistoryCreate
):

    db = SessionLocal()

    try:

        history = NotificationHistory(

            notification_id=payload.notification_id,

            user_id=payload.user_id,

            delivery_status=payload.delivery_status,

            delivered_at=datetime.utcnow()
        )

        db.add(history)

        db.commit()

        return success_response(
            message="Notification history created"
        )

    except Exception as e:

        db.rollback()

        return error_response(
            message="Failed to create history",
            details=str(e)
        )

    finally:

        db.close()

def get_notification_history(
    user_id: int
):

    db = SessionLocal()

    try:

        history = db.query(
            NotificationHistory
        ).filter(
            NotificationHistory.user_id == user_id
        ).all()

        return success_response(
            message="Notification history retrieved",
            data=history
        )

    finally:

        db.close()

def get_role_notifications(
    organization_id: int,
    role: str
):

    db = SessionLocal()

    try:

        notifications = db.query(
            Notifications
        ).filter(
            Notifications.organization_id == organization_id,
            Notifications.target_role == role
        ).all()

        return success_response(
            message="Role notifications retrieved",
            data=notifications
        )

    finally:

        db.close()
        
def get_organization_announcements(
    organization_id: int
):

    db = SessionLocal()

    try:

        announcements = db.query(
            Notifications
        ).filter(
            Notifications.organization_id == organization_id,
            Notifications.target_role == "ALL"
        ).all()

        return success_response(
            message="Announcements retrieved",
            data=announcements
        )

    finally:

        db.close()                                        