from app.db.session import SessionLocal
from app.models.kpis import Kpis
from app.schemas.kpi import KPICreate
from app.utils.response import success_response, error_response
from datetime import datetime
from app.models.kpi_values import KPIValues
from app.models.kpi_alerts import KPIAlerts

def create_kpi(payload: KPICreate):

    db = SessionLocal()

    try:

        kpi = KPIS(
            organization_id=payload.organization_id,
            name=payload.name,
            description=payload.description,
            category=payload.category,
            unit=payload.unit,
            target_value=payload.target_value,
            warning_threshold=payload.warning_threshold,
            critical_threshold=payload.critical_threshold,
            is_active="Yes",
            created_by="System"
        )

        db.add(kpi)
        db.commit()

        return success_response(
            message="KPI created successfully"
        )

    except Exception as e:

        db.rollback()

        return error_response(
            message="Failed to create KPI",
            details=str(e)
        )

    finally:

        db.close()

def get_all_kpis():

    db = SessionLocal()

    try:

        kpis = db.query(KPIS).all()

        return success_response(
            message="KPIs retrieved successfully",
            data=kpis
        )

    finally:

        db.close()

def create_kpi_value(payload: KPIValueCreate):

    db = SessionLocal()

    try:

        value = KPIValues(
            kpi_id=payload.kpi_id,
            organization_id=payload.organization_id,
            value=payload.value,
            notes=payload.notes,
            measurement_date=datetime.utcnow()
        )

        db.add(value)
        db.commit()

        return success_response(
            message="KPI value added successfully"
        )

    except Exception as e:

        db.rollback()

        return error_response(
            message="Failed to add KPI value",
            details=str(e)
        )

    finally:

        db.close()
        
def get_kpi_trends(kpi_id: int):

    db = SessionLocal()

    try:

        values = (
            db.query(KPIValues)
            .filter(KPIValues.kpi_id == kpi_id)
            .all()
        )

        return success_response(
            message="KPI trend retrieved",
            data=values
        )

    finally:

        db.close()                        

def get_kpi_performance(kpi_id: int):

    db = SessionLocal()

    try:

        kpi = (
            db.query(KPIS)
            .filter(KPIS.id == kpi_id)
            .first()
        )

        latest_value = (
            db.query(KPIValues)
            .filter(KPIValues.kpi_id == kpi_id)
            .order_by(KPIValues.measurement_date.desc())
            .first()
        )

        if not kpi or not latest_value:

            return error_response(
                message="KPI data not found"
            )

        achievement = (
            float(latest_value.value)
            / float(kpi.target_value)
        ) * 100

        return success_response(
            message="KPI performance calculated",
            data={
                "target": kpi.target_value,
                "current": latest_value.value,
                "achievement_percentage": round(
                    achievement, 2
                )
            }
        )

    finally:

        db.close()
        
def generate_kpi_report(kpi_id: int):

    performance = get_kpi_performance(kpi_id)

    return success_response(
        message="KPI report generated",
        data=performance["data"]
    )


def generate_kpi_alerts(kpi_id: int):

    db = SessionLocal()

    try:

        kpi = db.query(KPIS).filter(
            KPIS.id == kpi_id
        ).first()

        latest = (
            db.query(KPIValues)
            .filter(KPIValues.kpi_id == kpi_id)
            .order_by(
                KPIValues.measurement_date.desc()
            )
            .first()
        )

        if not kpi or not latest:

            return error_response(
                message="KPI data not found"
            )

        current = float(latest.value)

        if current <= float(kpi.critical_threshold):

            alert_type = "Critical"

        elif current <= float(kpi.warning_threshold):

            alert_type = "Warning"

        else:

            return success_response(
                message="No KPI alerts triggered"
            )

        alert = KPIAlerts(
            kpi_id=kpi.id,
            organization_id=kpi.organization_id,
            alert_type=alert_type,
            threshold_value=(
                kpi.critical_threshold
                if alert_type == "Critical"
                else kpi.warning_threshold
            ),
            current_value=current,
            status="Open",
            triggered_at=datetime.utcnow()
        )

        db.add(alert)
        db.commit()

        return success_response(
            message="KPI alert generated"
        )

    except Exception as e:

        db.rollback()

        return error_response(
            message="Failed to generate alert",
            details=str(e)
        )

    finally:

        db.close()                    