from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.security import verify_role
from app.models.alert_settings import AlertSettings
from app.utils.response import success_response
from app.schemas.alert_settings import AlertSettingsUpdate

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.get(
    "/alert-settings"
)
def get_alert_settings(
    db: Session = Depends(get_db),
    user = Depends(verify_role("admins"))
):
    settings = db.query(AlertSettings).first()
    return success_response(

        message="Settings loaded",

        data=settings
)

@router.put(
    "/alert-settings"
)
def update_alert_settings(

    payload: AlertSettingsUpdate,

    db: Session = Depends(get_db),

    user = Depends(verify_role("admins"))

):
    settings = db.query(AlertSettings).first()
    settings.high_demand_threshold = payload.high_demand_threshold

    settings.low_stock_threshold = payload.low_stock_threshold

    settings.email_notifications = payload.email_notifications

    settings.forecast_failure_notifications = payload.forecast_failure_notifications

    settings.report_completion_notifications = payload.report_completion_notifications
    db.commit()
    db.refresh(settings)        
    
    return success_response(

    message="Settings updated",

    data=settings
)