from pydantic import BaseModel

class NotificationCreate(BaseModel):

    organization_id: int

    title: str

    message: str

    notification_type: str

    target_role: str

    status: str

    created_by: str

class NotificationPreferenceCreate(BaseModel):

    user_id: int

    email_enabled: bool

    in_app_enabled: bool

    forecast_alerts: bool

    workflow_alerts: bool

    report_alerts: bool    

class NotificationHistoryCreate(BaseModel):

    notification_id: int

    user_id: int

    delivery_status: str    