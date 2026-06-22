from fastapi import APIRouter, Depends
from app.core.security import verify_role
from app.schemas.workflow import (
    WorkflowCreate,
    WorkflowStepCreate,
    WorkflowExecutionCreate
)

from app.services.workflow_service import (
    create_workflow,
    get_workflows,
    create_workflow_step,
    execute_workflow,
    get_workflow_executions,
    get_workflow_logs
)

router = APIRouter(
    prefix="/workflow",
    tags=["Workflow Automation"]
)

@router.post("/")
def add_new_workflow(
    workflow: WorkflowCreate,
    user = Depends(verify_role("admins"))
):
    return create_workflow(
        workflow
    )


@router.get("/")
def list_all_workflows(
    user = Depends(verify_role("manager"))
):
    return get_workflows()


@router.post("/steps")
def add_step(
    step: WorkflowStepCreate,
    user = Depends(verify_role("manager"))
):
    return create_workflow_step(
        step
    )


@router.post("/execute")
def execute(
    execution: WorkflowExecutionCreate,
    user = Depends(verify_role("manager"))
):
    return execute_workflow(
        execution
    )

@router.get("/executions")
def get_executions(
    user = Depends(verify_role("manager"))
):
    return get_workflow_executions()


@router.get("/logs")
def get_logs(
    user = Depends(verify_role("manager"))
):
    return get_workflow_logs()