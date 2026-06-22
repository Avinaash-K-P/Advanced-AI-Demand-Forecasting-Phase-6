from pydantic import BaseModel
from typing import Optional

class ForecastLifecycleUpdate(BaseModel):

    forecast_id: int
    status: str
    performed_by: str

class GovernanceAuditLogCreate(BaseModel):

    organization_id: int

    entity_type: str
    entity_id: int

    action: str

    performed_by: str

    old_value: Optional[str] = None
    new_value: Optional[str] = None


class GovernanceDashboardRequest(BaseModel):

    organization_id: int


class ForecastVersionRequest(BaseModel):

    forecast_date: str


class ActivityTimelineRequest(BaseModel):

    project_id: Optional[int] = None
    forecast_id: Optional[int] = None