from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.utils.response import success_response, error_response

from app.models.forecast_approval import ForecastApproval
from app.models.forecast_approval_history import ForecastApprovalHistory
from app.models.forecast_results import ForecastResult

from app.schemas.forecast_approval import (
    ForecastApprovalCreate,
    ForecastApprovalReview,
    ForecastApprovalUpdate
)

from datetime import datetime

def submit_forecast_for_approval(
    approval_data: ForecastApprovalCreate
):

    db = SessionLocal()

    try:

        forecast = (
            db.query(ForecastResult)
            .filter(
                ForecastResult.id == approval_data.forecast_id
            )
            .first()
        )

        if not forecast:

            return error_response(
                message="Forecast not found"
            )

        approval = ForecastApproval(
            forecast_id=approval_data.forecast_id,
            organization_id=approval_data.organization_id,
            submitted_by=approval_data.submitted_by,
            assigned_reviewer=approval_data.assigned_reviewer,
            status="Submitted",
            comments=approval_data.comments
        )

        db.add(approval)

        forecast.approval_status  = "Submitted" # type: ignore

        db.flush()

        history = ForecastApprovalHistory(
            forecast_approval_id=approval.id,
            forecast_id=approval_data.forecast_id,
            action_by=approval_data.submitted_by,
            old_status="Draft",
            new_status="Submitted",
            remarks="Forecast submitted for approval",
            action_date=datetime.utcnow()
        )

        db.add(history)

        db.commit()

        return success_response(
            message="Forecast submitted for approval successfully"
        )

    except Exception as e:

        db.rollback()

        return error_response(
            message="Failed to submit forecast",
            details=str(e)
        )

    finally:

        db.close()

def approve_forecast(
    approval_id: int,
    review_data: ForecastApprovalReview
):

    db = SessionLocal()

    try:

        approval = (
            db.query(ForecastApproval)
            .filter(
                ForecastApproval.id == approval_id
            )
            .first()
        )

        if not approval:

            return error_response(
                message="Approval request not found"
            )

        forecast = (
            db.query(ForecastResult)
            .filter(
                ForecastResult.id == approval.forecast_id
            )
            .first()
        )

        old_status = approval.status

        approval.status = "Approved"# type: ignore

        approval.reviewed_at = datetime.utcnow()# type: ignore


        forecast.approval_status = "Approved"# type: ignore


        history = ForecastApprovalHistory(
            forecast_approval_id=approval.id,
            forecast_id=approval.forecast_id,
            action_by=review_data.action_by,
            old_status=old_status,
            new_status="Approved",
            remarks=review_data.remarks,
            action_date=datetime.utcnow()
        )

        db.add(history)

        db.commit()

        return success_response(
            message="Forecast approved successfully"
        )

    except Exception as e:

        db.rollback()

        return error_response(
            message="Failed to approve forecast",
            details=str(e)
        )

    finally:

        db.close()

def reject_forecast(
    approval_id: int,
    review_data: ForecastApprovalReview
):

    db = SessionLocal()

    try:

        approval = (
            db.query(ForecastApproval)
            .filter(
                ForecastApproval.id == approval_id
            )
            .first()
        )

        if not approval:

            return error_response(
                message="Approval request not found"
            )

        forecast = (
            db.query(ForecastResult)
            .filter(
                ForecastResult.id == approval.forecast_id
            )
            .first()
        )

        old_status = approval.status

        approval.status = "Rejected"# type: ignore

        approval.reviewed_at = datetime.utcnow()# type: ignore


        forecast.approval_status = "Rejected" # type: ignore

        history = ForecastApprovalHistory(
            forecast_approval_id=approval.id,
            forecast_id=approval.forecast_id,
            action_by=review_data.action_by,
            old_status=old_status,
            new_status="Rejected",
            remarks=review_data.remarks,
            action_date=datetime.utcnow()
        )

        db.add(history)

        db.commit()

        return success_response(
            message="Forecast rejected successfully"
        )

    except Exception as e:

        db.rollback()

        return error_response(
            message="Failed to reject forecast",
            details=str(e)
        )

    finally:

        db.close()

def get_approval_history(
    forecast_id: int
):

    db = SessionLocal()

    try:

        history = (
            db.query(ForecastApprovalHistory)
            .filter(
                ForecastApprovalHistory.forecast_id == forecast_id
            )
            .all()
        )

        return success_response(
            message="Approval history retrieved successfully",
            data=history
        )

    except Exception as e:

        return error_response(
            message="Failed to retrieve approval history",
            details=str(e)
        )

    finally:

        db.close()

def get_pending_approvals():

    db = SessionLocal()

    try:

        approvals = (
            db.query(ForecastApproval)
            .filter(
                ForecastApproval.status == "Submitted"
            )
            .all()
        )

        return success_response(
            message="Pending approvals retrieved successfully",
            data=approvals
        )

    except Exception as e:

        return error_response(
            message="Failed to retrieve pending approvals",
            details=str(e)
        )

    finally:

        db.close()