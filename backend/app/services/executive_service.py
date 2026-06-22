from app.db.session import SessionLocal

from app.models.user import User
from app.models.forecast_results import ForecastResult
from app.models.reports import Report

from app.models.kpis import Kpis
from app.models.kpi_alerts import KPIAlerts

from app.models.workflow import Workflow

from app.models.annual_plans import AnnualPlans
from app.models.quarterly_plans import QuarterlyPlans
from app.models.business_targets import BusinessTargets

from app.models.executive_dashboard import ExecutiveDashboard
from app.models.executive_alerts import ExecutiveAlerts

from app.utils.response import (
    success_response,
    error_response
)

def get_executive_dashboard(
    organization_id: int
):

    db = SessionLocal()

    try:

        total_users = db.query(User).filter(
            User.organization_id == organization_id
        ).count()

        total_forecasts = db.query(ForecastResult).filter(
            ForecastResult.organization_id == organization_id
        ).count()

        total_reports = db.query(Report).filter(
            Report.organization_id == organization_id
        ).count()

        total_kpis = db.query(Kpis).filter(
            Kpis.organization_id == organization_id
        ).count()

        active_workflows = db.query(Workflow).filter(
            Workflow.organization_id == organization_id,
            Workflow.is_active == "Yes"
        ).count()

        return success_response(
            message="Executive dashboard retrieved",
            data={
                "total_users": total_users,
                "total_forecasts": total_forecasts,
                "total_reports": total_reports,
                "total_kpis": total_kpis,
                "active_workflows": active_workflows
            }
        )

    finally:

        db.close()

def get_forecast_metrics(
    organization_id: int
):

    db = SessionLocal()

    try:

        forecasts = db.query(ForecastResult).filter(
            ForecastResult.organization_id == organization_id
        ).all()

        total_forecasts = len(forecasts)

        approved = sum(
            1 for f in forecasts
            if f.approval_status == "Approved"
        )

        rejected = sum(
            1 for f in forecasts
            if f.approval_status == "Rejected"
        )

        avg_confidence = 0

        if forecasts:

            avg_confidence = round(
                sum(
                    f.confidence_score
                    for f in forecasts
                ) / len(forecasts),
                2
            )

        return success_response(
            message="Forecast metrics retrieved",
            data={
                "total_forecasts": total_forecasts,
                "approved_forecasts": approved,
                "rejected_forecasts": rejected,
                "average_confidence": avg_confidence
            }
        )

    finally:

        db.close()        

def get_planning_insights(
    organization_id: int
):

    db = SessionLocal()

    try:

        annual_plans = db.query(
            AnnualPlans
        ).filter(
            AnnualPlans.organization_id == organization_id
        ).count()

        quarterly_plans = db.query(
            QuarterlyPlans
        ).filter(
            QuarterlyPlans.organization_id == organization_id
        ).count()

        targets = db.query(
            BusinessTargets
        ).filter(
            BusinessTargets.organization_id == organization_id
        ).count()

        return success_response(
            message="Planning insights retrieved",
            data={
                "annual_plans": annual_plans,
                "quarterly_plans": quarterly_plans,
                "business_targets": targets
            }
        )

    finally:

        db.close()

def get_business_summary(
    organization_id: int
):

    db = SessionLocal()

    try:

        total_kpis = db.query(Kpis).filter(
            Kpis.organization_id == organization_id
        ).count()

        active_alerts = db.query(KPIAlerts).filter(
            KPIAlerts.organization_id == organization_id,
            KPIAlerts.status == "Open"
        ).count()

        critical_alerts = db.query(KPIAlerts).filter(
            KPIAlerts.organization_id == organization_id,
            KPIAlerts.alert_type == "Critical"
        ).count()

        return success_response(
            message="Business summary retrieved",
            data={
                "total_kpis": total_kpis,
                "active_alerts": active_alerts,
                "critical_alerts": critical_alerts
            }
        )

    finally:

        db.close()

def create_executive_alert(
    payload
):

    db = SessionLocal()

    try:

        alert = ExecutiveAlerts(

            organization_id=payload.organization_id,

            alert_type=payload.alert_type,

            severity=payload.severity,

            message=payload.message,

            status=payload.status
        )

        db.add(alert)

        db.commit()

        return success_response(
            message="Executive alert created"
        )

    except Exception as e:

        db.rollback()

        return error_response(
            message="Failed to create alert",
            details=str(e)
        )

    finally:

        db.close()

def get_executive_alerts(
    organization_id: int
):

    db = SessionLocal()

    try:

        alerts = db.query(
            ExecutiveAlerts
        ).filter(
            ExecutiveAlerts.organization_id
            == organization_id
        ).all()

        return success_response(
            message="Executive alerts retrieved",
            data=alerts
        )

    finally:

        db.close()       
