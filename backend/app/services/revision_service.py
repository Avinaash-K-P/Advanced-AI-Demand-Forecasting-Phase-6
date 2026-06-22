from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.forecast_revision import ForecastRevision
from app.models.forecast_results import ForecastResult
from app.utils.timeline_logger import log_timeline_event, TimelineAction, TimelineCategory


def snapshot_forecast_revision(
    db: Session,
    user_id: int = None,
    project_id: int = None
):
    """
    Called before forecast_results is wiped in auto_generate_forecast().
    Takes a full snapshot of current forecast_results as a new revision.
    Automatically computes change_summary vs previous revision.
    """

    current_results = db.query(ForecastResult).all()

    if not current_results:
        return

    for row in current_results:

        # Get next revision number for this forecast_date
        last_revision = db.query(
            func.max(ForecastRevision.revision_number)
        ).filter(
            ForecastRevision.forecast_date == row.forecast_date
        ).scalar()

        next_revision = (last_revision or 0) + 1

        # Build change summary vs previous revision
        change_summary = _build_change_summary(db, row, next_revision)

        revision = ForecastRevision(
            revision_number=next_revision,
            forecast_date=row.forecast_date,
            predicted_demand=row.predicted_demand,
            prophet_prediction=row.prophet_prediction,
            lr_prediction=row.lr_prediction,
            ma_prediction=row.ma_prediction,
            sales_trend=row.sales_trend,
            weekly_pattern=row.weekly_pattern,
            yearly_pattern=row.yearly_pattern,
            confidence_score=row.confidence_score,
            model_type="Ensemble",
            change_summary=change_summary,
            created_by=user_id,
            project_id=project_id
        )

        db.add(revision)

    db.commit()

    # Log to timeline
    if user_id:
        total = len(current_results)
        log_timeline_event(
            db=db,
            user_id=user_id,
            action=TimelineAction.REVISION_SAVED,
            category=TimelineCategory.FORECAST,
            project_id=project_id,
            description=f"Forecast revision snapshot saved — {total} records",
            meta_value=f"revision saved"
        )


def _build_change_summary(
    db: Session,
    current_row: ForecastResult,
    next_revision: int
) -> str:
    """
    Compares current forecast row to the previous revision for the same date.
    Returns a human-readable change summary string.
    """

    if next_revision == 1:
        return "Initial forecast revision"

    previous = db.query(ForecastRevision).filter(
        ForecastRevision.forecast_date == current_row.forecast_date,
        ForecastRevision.revision_number == next_revision - 1
    ).first()

    if not previous:
        return "No previous revision found for comparison"

    prev_demand = previous.predicted_demand
    curr_demand = current_row.predicted_demand

    if prev_demand and prev_demand != 0:
        change = curr_demand - prev_demand
        change_pct = round((change / prev_demand) * 100, 2)
        direction = "increased" if change > 0 else "decreased"
        return (
            f"Predicted demand {direction} by "
            f"{abs(round(change, 2))} units "
            f"({abs(change_pct)}%) from revision {next_revision - 1}"
        )

    return "Previous demand was zero — cannot compute percentage change"


def get_revisions_by_date(
    db: Session,
    forecast_date: str
):
    """Get all revisions for a specific forecast date."""
    return db.query(ForecastRevision).filter(
        ForecastRevision.forecast_date == forecast_date
    ).order_by(ForecastRevision.revision_number.asc()).all()


def get_latest_revision(
    db: Session,
    forecast_date: str
):
    """Get the latest revision for a specific forecast date."""
    return db.query(ForecastRevision).filter(
        ForecastRevision.forecast_date == forecast_date
    ).order_by(ForecastRevision.revision_number.desc()).first()


def compare_revisions(
    db: Session,
    forecast_date: str,
    revision_a: int,
    revision_b: int
):
    """
    Compare two specific revisions for the same forecast date.
    Returns delta values between revision_a and revision_b.
    """

    rev_a = db.query(ForecastRevision).filter(
        ForecastRevision.forecast_date == forecast_date,
        ForecastRevision.revision_number == revision_a
    ).first()

    rev_b = db.query(ForecastRevision).filter(
        ForecastRevision.forecast_date == forecast_date,
        ForecastRevision.revision_number == revision_b
    ).first()

    if not rev_a or not rev_b:
        return None

    demand_change = round(rev_b.predicted_demand - rev_a.predicted_demand, 2)
    demand_change_pct = round(
        ((demand_change / rev_a.predicted_demand) * 100)
        if rev_a.predicted_demand else 0, 2
    )
    confidence_change = round(rev_b.confidence_score - rev_a.confidence_score, 2)
    trend_change = round(rev_b.sales_trend - rev_a.sales_trend, 2)

    return {
        "forecast_date": forecast_date,
        "revision_a": revision_a,
        "revision_b": revision_b,
        "demand_change": demand_change,
        "demand_change_pct": demand_change_pct,
        "confidence_change": confidence_change,
        "trend_change": trend_change
    }