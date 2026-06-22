from pydantic import BaseModel
from typing import Optional


class ForecastApprovalCreate(BaseModel):
    forecast_id: int
    organization_id: int
    submitted_by: str
    assigned_reviewer: str
    comments: Optional[str] = None


class ForecastApprovalReview(BaseModel):
    action: str
    action_by: str
    remarks: Optional[str] = None


class ForecastApprovalUpdate(BaseModel):
    assigned_reviewer: Optional[str] = None
    comments: Optional[str] = None