from datetime import datetime
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.sales import Sales
from app.models.user import User
from app.models.forecast_results import ForecastResult
from app.models.model_metadata import ModelMetadata
# ── Modular Services ──
from app.services.preprocessing_service import preprocess_sales_data
from app.services.training_service import (
    train_prophet,
    train_linear_regression,
    compute_moving_average,
    build_ensemble_forecast
)
from app.services.evaluation_service import evaluate_forecast_accuracy
from app.services.alert_service import (
    generate_forecast_alerts,
    generate_failure_alert,
    generate_completion_alert
)
from app.services.revision_service import snapshot_forecast_revision

# Auto Generate sales data and forecast reports
def auto_generate_forecast(org_id:int):
    """
    Orchestrates the full forecast pipeline:
    1. Preprocess sales data
    2. Train all models
    3. Build ensemble forecast
    4. Snapshot existing results (revision history)
    5. Save new forecast results (bulk insert)
    6. Evaluate accuracy
    7. Update model metadata
    8. Generate alerts
    """
 
    db = SessionLocal()
 
    try:
 
        print("Starting forecast pipeline...")
 
        # 1. Load + preprocess
        sales_data = (
        db.query(Sales)
            .filter(
                Sales.organization_id == org_id
            )
        .all()
)
 
        if not sales_data:
            print("No sales data found. Skipping forecast.")
            return
 
        df = preprocess_sales_data(sales_data)
 
        # 2. Train models
        _, prophet_forecast    = train_prophet(df)
        lr_predictions         = train_linear_regression(df)
        moving_average         = compute_moving_average(df)
 
        # 3. Build ensemble
        result_df = build_ensemble_forecast(
            df, prophet_forecast, lr_predictions, moving_average
        )
 
        # 4. Snapshot before wipe (revision history)
        print("Saving revision snapshot...")
        snapshot_forecast_revision(db=db, user_id=None, project_id=None) # type: ignore
 
        # 5. Wipe + bulk insert new forecast
        db.query(ForecastResult).delete()
        db.commit()

        new_records = [
            ForecastResult(
                organization_id = org_id,
                forecast_date=row["ds"],
                predicted_demand=row["predicted_demand"],
                prophet_prediction=row["prophet_prediction"],
                lr_prediction=row["lr_prediction"],
                ma_prediction=row["ma_prediction"],
                sales_trend=row["sales_trend"],
                weekly_pattern=row["weekly_pattern"],
                yearly_pattern=row["yearly_pattern"],
                confidence_score=row["confidence_score"]
            )
            for row in result_df.to_dict(orient="records")
        ]
 
        db.bulk_save_objects(new_records)
        db.commit()
 
        # 6. Evaluate accuracy
        evaluate_forecast_accuracy(db)
 
        # 7. Update model metadata
        current_count = db.query(Sales).count()
        metadata = db.query(ModelMetadata).first()
 
        if not metadata:
            metadata = ModelMetadata(last_sales_count=current_count)
            db.add(metadata)
        elif current_count > metadata.last_sales_count:
            metadata.last_sales_count = current_count
            metadata.last_trained_at  = datetime.utcnow()
 
        db.commit()
 
        # 8. Alerts
        generate_forecast_alerts(db)
 
        print("Forecast pipeline completed successfully.")
 
    except Exception as e:
 
        print("FORECAST PIPELINE ERROR:", e)
        generate_failure_alert(db, str(e))
 
    finally:
 
        generate_completion_alert(db)
        db.close()




