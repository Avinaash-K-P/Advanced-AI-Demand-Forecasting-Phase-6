from sqlalchemy.orm import Session
from app.models.forecast_results import ForecastResult
from app.models.alerts import Alert
from app.models.alert_settings import AlertSettings


def generate_forecast_alerts(db: Session):
    """
    Scans forecast results against alert thresholds
    and creates alert records for high demand dates.
    """

    settings = db.query(AlertSettings).first()

    if not settings:
        return

    forecast_rows = db.query(ForecastResult).all()

    alerts = []

    for row in forecast_rows:

        if row.predicted_demand > settings.high_demand_threshold:

            alerts.append(Alert(
                alert_type="High Demand",
                severity="High",
                message=(
                    f"Predicted demand ({round(row.predicted_demand, 2)}) "
                    f"exceeded threshold ({settings.high_demand_threshold}) "
                    f"on {row.forecast_date}"
                )
            ))

    if alerts:
        db.bulk_save_objects(alerts)
        db.commit()


def generate_failure_alert(db: Session, error_message: str):
    """Creates a forecast failure alert."""

    try:
        settings = db.query(AlertSettings).first()
        if settings and settings.forecast_failure_notifications:
            alert = Alert(
                alert_type="Forecast Failure",
                severity="High",
                message=f"Forecast generation failed: {error_message}"
            )
            db.add(alert)
            db.commit()
    except Exception as e:
        print("ALERT CREATION ERROR:", e)


def generate_completion_alert(db: Session):
    """Creates a report ready alert after successful forecast."""

    try:
        settings = db.query(AlertSettings).first()
        if settings and settings.report_completion_notifications:
            alert = Alert(
                alert_type="Report Ready",
                severity="Low",
                message="Forecast report generated successfully."
            )
            db.add(alert)
            db.commit()
    except Exception as e:
        print("COMPLETION ALERT ERROR:", e)