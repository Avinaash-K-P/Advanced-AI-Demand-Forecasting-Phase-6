from pydantic import BaseModel
from typing import Optional


# Annual Plans

class AnnualPlanCreate(BaseModel):

    organization_id: int
    year: str
    name: str
    description: Optional[str] = None
    status: str
    created_by: str


class AnnualPlanUpdate(BaseModel):

    year: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


# Quarterly Plans

class QuarterlyPlanCreate(BaseModel):

    organization_id: int
    annual_plan_id: int
    quarter: str
    year: str
    name: str
    description: Optional[str] = None
    status: str


class QuarterlyPlanUpdate(BaseModel):

    quarter: Optional[str] = None
    year: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


# Business Targets

class BusinessTargetCreate(BaseModel):

    organization_id: int
    annual_plan_id: int
    quarterly_plan_id: int

    target_name: str
    target_type: str

    target_value: float
    current_value: float = 0

    unit: str
    status: str


class BusinessTargetUpdate(BaseModel):

    target_name: Optional[str] = None
    target_type: Optional[str] = None

    target_value: Optional[float] = None
    current_value: Optional[float] = None

    unit: Optional[str] = None
    status: Optional[str] = None


# Planning Recommendation

class PlanningRecommendationRequest(BaseModel):

    organization_id: int