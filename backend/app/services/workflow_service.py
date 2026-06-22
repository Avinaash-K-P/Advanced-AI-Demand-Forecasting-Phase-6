from datetime import datetime

from app.db.session import SessionLocal

from app.models.workflow import Workflow
from app.models.workflow_steps import Workflowsteps
from app.models.workflow_executions import WorkflowExecution
from app.models.workflow_logs import WorkflowLogs

from app.schemas.workflow import (
    WorkflowCreate,
    WorkflowUpdate,
    WorkflowStepCreate,
    WorkflowExecutionCreate
)

from app.utils.response import (
    success_response,
    error_response
)

def create_workflow(
    workflow_data: WorkflowCreate
):

    db = SessionLocal()

    try:

        workflow = Workflow(
            organization_id=workflow_data.organization_id,
            name=workflow_data.name,
            description=workflow_data.description,
            workflow_type=workflow_data.workflow_type,
            trigger_event=workflow_data.trigger_event,
            is_active=workflow_data.is_active,
            created_by=workflow_data.created_by
        )

        db.add(workflow)
        db.commit()
        db.refresh(workflow)

        return success_response(
            message="Workflow created successfully",
            data={
                "workflow_id": workflow.id
            }
        )

    except Exception as e:

        db.rollback()

        return error_response(
            message="Failed to create workflow",
            details=str(e)
        )

    finally:

        db.close()

def get_workflows():

    db = SessionLocal()

    try:

        workflows = db.query(
            Workflow
        ).all()

        return success_response(
            message="Workflows retrieved successfully",
            data=workflows
        )

    except Exception as e:

        return error_response(
            message="Failed to retrieve workflows",
            details=str(e)
        )

    finally:

        db.close()        

def create_workflow_step(
    step_data: WorkflowStepCreate
):

    db = SessionLocal()

    try:

        workflow = (
            db.query(Workflow)
            .filter(
                Workflow.id == step_data.workflow_id
            )
            .first()
        )

        if not workflow:

            return error_response(
                message="Workflow not found"
            )

        step = Workflowsteps(
            workflow_id=step_data.workflow_id,
            step_order=step_data.step_order,
            step_name=step_data.step_name,
            step_type=step_data.step_type,
            configuration=step_data.configuration,
            is_required=step_data.is_required
        )

        db.add(step)
        db.commit()

        return success_response(
            message="Workflow step created successfully"
        )

    except Exception as e:

        db.rollback()

        return error_response(
            message="Failed to create workflow step",
            details=str(e)
        )

    finally:

        db.close()

def execute_workflow(
    execution_data: WorkflowExecutionCreate
):

    db = SessionLocal()

    try:

        workflow = (
            db.query(Workflow)
            .filter(
                Workflow.id == execution_data.workflow_id
            )
            .first()
        )

        if not workflow:

            return error_response(
                message="Workflow not found"
            )

        execution = WorkflowExecution(
            workflow_id=execution_data.workflow_id,
            organization_id=execution_data.organization_id,
            status="Running",
            started_at=datetime.utcnow(),
            triggered_by=execution_data.triggered_by,
            execution_context=execution_data.execution_context
        )

        db.add(execution)

        db.flush()

        log = WorkflowLogs(
            workflow_execution_id=execution.id,
            workflow_step_id="START",
            log_level="INFO",
            message="Workflow execution started"
        )

        db.add(log)

        execution.status = "Completed"  #type: ignore
        execution.completed_at = datetime.utcnow() #type: ignore

        db.commit()

        return success_response(
            message="Workflow executed successfully",
            data={
                "execution_id": execution.id
            }
        )

    except Exception as e:

        db.rollback()

        return error_response(
            message="Workflow execution failed",
            details=str(e)
        )

    finally:

        db.close()

def get_workflow_executions():

    db = SessionLocal()

    try:

        executions = (
            db.query(
                WorkflowExecution
            )
            .all()
        )

        return success_response(
            message="Workflow executions retrieved successfully",
            data=executions
        )

    except Exception as e:

        return error_response(
            message="Failed to retrieve executions",
            details=str(e)
        )

    finally:

        db.close()                

def get_workflow_logs():

    db = SessionLocal()

    try:

        logs = (
            db.query(
                WorkflowLogs
            )
            .all()
        )

        return success_response(
            message="Workflow logs retrieved successfully",
            data=logs
        )

    except Exception as e:

        return error_response(
            message="Failed to retrieve workflow logs",
            details=str(e)
        )

    finally:

        db.close()