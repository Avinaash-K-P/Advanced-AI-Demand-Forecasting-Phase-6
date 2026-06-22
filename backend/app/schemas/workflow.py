from pydantic import BaseModel
from typing import Optional

class WorkflowCreate(BaseModel):

    organization_id: int
    name: str
    description: Optional[str] = None
    workflow_type: str
    trigger_event: str
    is_active: bool
    created_by: str


class WorkflowUpdate(BaseModel):

    name: Optional[str] = None
    description: Optional[str] = None
    workflow_type: Optional[str] = None
    trigger_event: Optional[str] = None
    is_active: bool | None = None


class WorkflowStepCreate(BaseModel):

    workflow_id: int
    step_order: str
    step_name: str
    step_type: str
    configuration: Optional[str] = None
    is_required: str


class WorkflowStepUpdate(BaseModel):

    step_order: Optional[str] = None
    step_name: Optional[str] = None
    step_type: Optional[str] = None
    configuration: Optional[str] = None
    is_required: Optional[str] = None


class WorkflowExecutionCreate(BaseModel):

    workflow_id: int
    organization_id: int
    triggered_by: str
    execution_context: Optional[str] = None

class WorkflowLogCreate(BaseModel):

    workflow_execution_id: int
    workflow_step_id: str
    log_level: str
    message: str