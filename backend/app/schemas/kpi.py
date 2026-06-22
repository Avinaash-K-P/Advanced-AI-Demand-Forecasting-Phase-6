from pydantic import BaseModel

class KPICreate(BaseModel):
    organization_id: int
    name: str
    description: str
    category: str
    unit: str
    target_value: float
    warning_threshold: float
    critical_threshold: float

class KPIValueCreate(BaseModel):
    kpi_id: int
    organization_id: int
    value: float
    notes: str | None = None

class KPIAlertCreate(BaseModel):
    kpi_id: int
    organization_id: int
    alert_type: str
    threshold_value: float
    current_value: float

class KPIUpdate(BaseModel):
    name: str
    description: str
    category: str
    unit: str
    target_value: float
    warning_threshold: float
    critical_threshold: float
    is_active: str            