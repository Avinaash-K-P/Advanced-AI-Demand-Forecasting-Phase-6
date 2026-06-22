from pydantic import BaseModel
from typing import Optional


class OrganizationSettingsCreate(BaseModel):
    organization_id: int
    timezone: Optional[str] = "UTC"
    currency: Optional[str] = "USD"
    forecast_retention_days: Optional[int] = 365
    default_forecast_model: Optional[str] = None
    notifications_enabled: Optional[bool] = True


class OrganizationSettingsUpdate(BaseModel):
    timezone: Optional[str] = None
    currency: Optional[str] = None
    forecast_retention_days: Optional[int] = None
    default_forecast_model: Optional[str] = None
    notifications_enabled: Optional[bool] = None