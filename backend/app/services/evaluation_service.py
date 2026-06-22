from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.sales import Sales
from app.models.forecast_results import ForecastResult
from app.models.forecast_accuracy import ForecastAccuracy


def evaluate_forecast_accuracy(db: Session):
    """
    Computes accuracy for each date where both
    actual sales and forecast predictions exist.
    Clears old accuracy records and writes fresh ones.
    """

    db.query(ForecastAccuracy).delete()
    db.commit()

    # Aggregate actual demand per date in one query
    daily_sales = (
        db.query(
            Sales.sales_date,
            func.sum(Sales.quantity_sold).label("actual_demand")
        )
        .group_by(Sales.sales_date)
        .all()
    )

    # Build forecast lookup
    forecast_lookup = {
        str(row.forecast_date): row.predicted_demand
        for row in db.query(ForecastResult).all()
    }

    records = []

    for sale in daily_sales:

        predicted = forecast_lookup.get(str(sale.sales_date))

        if predicted is None:
            continue

        actual    = float(sale.actual_demand)
        predicted = float(predicted)

        if actual == 0:
            continue

        error_pct    = (abs(actual - predicted) / actual) * 100
        accuracy_pct = round(max(0.0, 100.0 - error_pct), 2)

        records.append(ForecastAccuracy(
            evaluation_date=sale.sales_date,
            actual_demand=actual,
            predicted_demand=predicted,
            accuracy_percentage=accuracy_pct,
            model_type="Ensemble"
        ))

    # Bulk insert — faster than individual adds
    if records:
        db.bulk_save_objects(records)
        db.commit()