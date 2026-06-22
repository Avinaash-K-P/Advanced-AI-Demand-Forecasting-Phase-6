from datetime import datetime

from app.db.session import SessionLocal

from app.models.forecast_revision import ForecastRevision
from app.models.forecast_activity_timeline import ForecastActivityTimeline
from app.models.governance_audit_logs import GovernanceAuditLogs
from app.models.forecast_results import ForecastResult

from app.schemas.governance import (
    ForecastLifecycleUpdate,
    GovernanceAuditLogCreate
)

from app.utils.response import (
    success_response,
    error_response
)
from app.models.forecast_lifecycle import ForecastLifecycle

def get_forecast_versions(
    forecast_date: str
):
    db = SessionLocal()

    try:

        revisions = (
            db.query(ForecastRevision)
            .filter(
                ForecastRevision.forecast_date == forecast_date
            )
            .order_by(
                ForecastRevision.revision_number.desc()
            )
            .all()
        )

        return success_response(
            message="Forecast revisions retrieved successfully",
            data=revisions
        )

    except Exception as e:

        return error_response(
            message="Failed to retrieve forecast revisions",
            details=str(e)
        )

    finally:

        db.close()

def get_forecast_activity_timeline():

    db = SessionLocal()

    try:

        activities = (
            db.query(ForecastActivityTimeline)
            .order_by(
                ForecastActivityTimeline.timestamp.desc()
            )
            .all()
        )

        return success_response(
            message="Forecast activity timeline retrieved successfully",
            data=activities
        )

    except Exception as e:

        return error_response(
            message="Failed to retrieve activity timeline",
            details=str(e)
        )

    finally:

        db.close()

def get_governance_audit_logs():

    db = SessionLocal()

    try:

        logs = (
            db.query(GovernanceAuditLogs)
            .order_by(
                GovernanceAuditLogs.created_at.desc()
            )
            .all()
        )

        return success_response(
            message="Governance audit logs retrieved successfully",
            data=logs
        )

    except Exception as e:

        return error_response(
            message="Failed to retrieve audit logs",
            details=str(e)
        )

    finally:

        db.close()

def update_forecast_lifecycle(
    lifecycle_data: ForecastLifecycleUpdate
):

    db = SessionLocal()

    try:

        forecast = (
            db.query(ForecastResult)
            .filter(
                ForecastResult.id ==
                lifecycle_data.forecast_id
            )
            .first()
        )

        if not forecast:

            return error_response(
                message="Forecast not found"
            )

        old_status = forecast.approval_status

        
        # Update Forecast Status

        forecast.approval_status = lifecycle_data.status  # type: ignore

        
        # Lifecycle Tracking
        

        lifecycle = ForecastLifecycle(

            forecast_id=forecast.id,

            organization_id=forecast.organization_id,

            current_stage=lifecycle_data.status,

            entered_at=str(datetime.utcnow()),

            updated_by=lifecycle_data.performed_by,

            notes=f"Status changed from {old_status} to {lifecycle_data.status}"
        )

        db.add(lifecycle)

        
        # Governance Audit Log
        
        audit_log = GovernanceAuditLogs(

            organization_id=forecast.organization_id,

            entity_type="Forecast",

            entity_id=forecast.id,

            action="STATUS_CHANGE",

            performed_by=lifecycle_data.performed_by,

            old_value=old_status,

            new_value=lifecycle_data.status
        )

        db.add(audit_log)

        # Activity Timeline
        
        activity = ForecastActivityTimeline(

            forecast_id=forecast.id,

            project_id=None,

            user_id=1,  # temporary until auth integration

            action="STATUS_CHANGED",

            category="forecast",

            description=(
                f"Forecast status changed from "
                f"{old_status} to {lifecycle_data.status}"
            ),

            meta_value=lifecycle_data.status
        )

        db.add(activity)
    
        # Commit Everything Together
    
        db.commit()

        return success_response(
            message="Forecast lifecycle updated successfully"
        )

    except Exception as e:

        db.rollback()

        return error_response(
            message="Failed to update lifecycle",
            details=str(e)
        )

    finally:

        db.close()          

def get_governance_dashboard():

    db = SessionLocal()

    try:

        total_revisions = (
            db.query(ForecastRevision)
            .count()
        )

        total_activities = (
            db.query(ForecastActivityTimeline)
            .count()
        )

        total_audit_logs = (
            db.query(GovernanceAuditLogs)
            .count()
        )

        approved_forecasts = (
            db.query(ForecastResult)
            .filter(
                ForecastResult.approval_status ==
                "Approved"
            )
            .count()
        )

        pending_forecasts = (
            db.query(ForecastResult)
            .filter(
                ForecastResult.approval_status.in_(
                    ["Draft", "Submitted", "Under Review"]
                )
            )
            .count()
        )

        rejected_forecasts = (
            db.query(ForecastResult)
            .filter(
                ForecastResult.approval_status ==
                "Rejected"
            )
            .count()
        )

        return success_response(
            message="Governance dashboard retrieved successfully",
            data={
                "total_revisions": total_revisions,
                "total_activities": total_activities,
                "total_audit_logs": total_audit_logs,
                "approved_forecasts": approved_forecasts,
                "pending_forecasts": pending_forecasts,
                "rejected_forecasts": rejected_forecasts
            }
        )

    except Exception as e:

        return error_response(
            message="Failed to retrieve governance dashboard",
            details=str(e)
        )

    finally:

        db.close()        