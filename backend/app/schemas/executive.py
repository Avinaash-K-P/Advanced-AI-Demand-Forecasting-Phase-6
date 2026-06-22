from pydantic import BaseModel


class ExecutiveAlertCreate(BaseModel):

    organization_id: int

    alert_type: str

    severity: str

    message: str

    status: str

class ExecutiveAlertResponse(BaseModel):

    id: int

    organization_id: int

    alert_type: str

    severity: str

    message: str

    status: str

    class Config:

        from_attributes = True 

class ExecutiveDashboardResponse(BaseModel):

    total_users: int

    total_forecasts: int

    total_reports: int

    total_kpis: int

    active_workflows: int           