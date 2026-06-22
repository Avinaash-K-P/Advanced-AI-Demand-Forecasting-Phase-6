from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
from app.db.database import get_db
from app.models.user import User
from app.models.sales import Sales
from app.models.forecast_results import ForecastResult
from app.models.forecast_history import ForecastHistory
from app.models.forecast_scheduler import ForecastSchedule
from app.models.forecast_accuracy import ForecastAccuracy
from app.schemas.forecast import ForecastScheduleUpdate
from app.core.security import verify_role, get_current_user
from app.utils.response import error_response, success_response
from app.utils.logger import log_api_activity
from app.services.preprocessing_service import preprocess_sales_data
from app.services.training_service import (
    train_prophet,
    train_linear_regression,
    compute_moving_average,
    build_ensemble_forecast
)
from app.services.evaluation_service import evaluate_forecast_accuracy
from datetime import datetime
from fastapi_cache.decorator import cache
from app.utils.apscheduler import (
    scheduler,
    load_forecast_schedule
)

router = APIRouter(prefix="/forecast", tags=["Forecast"])

# Preprocess Sales Data
@router.get("/preprocess-data")
def preprocess_data(
    db: Session = Depends(get_db),
    user = Depends(verify_role("analyst")),
    current_user: User = Depends(get_current_user)
):

    sales_data = (
     db.query(Sales).filter
    (
        Sales.organization_id == current_user.organization_id
    ).all()
    )

    processed_df = preprocess_sales_data(sales_data)
    new_data = processed_df.to_dict(orient="records")
    data = new_data
    return success_response(
        message = "Data preprocessed successfully!",
        data = data
    )

#Generate Forecast
@router.get("/generate-forecast")
def generate_forecast(
    db: Session = Depends(get_db),
    user = Depends(verify_role("analyst")),
    current_user: User = Depends(get_current_user)
):   
    sales_data = (
    db.query(Sales).filter
    (
        Sales.organization_id == current_user.organization_id
    ).all()
    )

    # Preprocess dataset
    processed_df = preprocess_sales_data(sales_data)

    # Train forecasting model
    
    _, prophet_df = train_prophet(processed_df)
    lr_df = train_linear_regression(processed_df)
    ma_df = compute_moving_average(processed_df)

    esemble_df = build_ensemble_forecast(processed_df, prophet_df, lr_df, ma_df)

    forecast_df = esemble_df

     # Store forecast results
    forecast_records = []

    for _, row in forecast_df.iterrows():

        # Adding to forecast results     
        forecast = ForecastResult(

            organization_id = current_user.organization_id,

            forecast_date = row["ds"],

            predicted_demand = float(row["predicted_demand"]),

            prophet_prediction = float(row["prophet_prediction"]),

            lr_prediction = float(row["lr_prediction"]),

            ma_prediction = float(row["ma_prediction"]),
            
            sales_trend = float(row["sales_trend"]),

            weekly_pattern = float(row["weekly_pattern"]),

            yearly_pattern = float(row["yearly_pattern"])

        )

        forecast_records.append(forecast)

        # Adding to forecast history 
        history = ForecastHistory(

        forecast_date=str(row["ds"]),

        predicted_demand=float(row["predicted_demand"]),

        model_type="Ensemble Prophet",

        generated_by=user["username"]
        )
        
    db.add_all(forecast_records)    
    db.add(history)    
    db.commit()

    # Eavluating data
    evaluate_forecast_accuracy(db)

    log_api_activity(

        db=db,

        user_id = user["id"],

        username= user["username"],

        endpoint="/generate-forecast",

        method="GET",

        status="SUCCESS"
    )

    data = forecast_df.to_dict(orient="records")
    return success_response(
        message = "Forecast generated successfully!",
        data = data
    )


#Forecast Scheduler
@router.put("/forecast-schedule")
def update_forecast_schedule(

    schedule_data: ForecastScheduleUpdate,

    db: Session = Depends(get_db),

    user = Depends(
        verify_role("admin")
    )
):

    schedule = db.query(
        ForecastSchedule
    ).first()

    valid_types = ["minutes","hours","days","weeks"]

    if not schedule:

        schedule = ForecastSchedule(

            interval_type=schedule_data.interval_type,

            interval_value=schedule_data.interval_value,

            is_active=True,

            updated_at=datetime.utcnow()
        )

        db.add(schedule)

    else:

        schedule.interval_type = (
            schedule_data.interval_type
        )

        schedule.interval_value = (
            schedule_data.interval_value
        )

        schedule.updated_at = (
            datetime.utcnow()
        )

    db.commit()
    
    job = scheduler.get_job("forecast_job")

    if job:
        scheduler.remove_job("forecast_job")

    load_forecast_schedule()

    if schedule_data.interval_type not in valid_types:

        raise HTTPException(status_code=400,detail="Invalid interval type")

    return success_response(

        message="Forecast schedule updated successfully!",

        data={

            "interval_type":
            schedule.interval_type,

            "interval_value":
            schedule.interval_value
        }
    )
@router.get("/get-forecast-schedule")
def get_schedule(

    db: Session = Depends(get_db),

    user = Depends(
        verify_role("admins")
    )

):

    schedule = db.query(
        ForecastSchedule
    ).first()

    return success_response(

        message="Schedule fetched",

        data=schedule
    )

@router.get("/forecast-history")
def forecast_history(
    start_date:str = None,
    end_date:str = None,
    model_type:str = None,
    db: Session = Depends(get_db),
    user = Depends(verify_role("analyst"))
):
    query = db.query(ForecastHistory)

    if start_date:
        query = query.filter(ForecastHistory.forecast_date>=start_date)

    if end_date:
        query = query.filter(ForecastHistory.forecast_date<=end_date)

    if model_type:
        query = query.filter(ForecastHistory.model_type == model_type)        

    history = db.query(ForecastHistory).order_by(ForecastHistory.generated_at.desc()).all()

    data = []

    for item in history:

        data.append({

            "forecast_date": item.forecast_date,

            "predicted_demand": item.predicted_demand,

            "model_type": item.model_type,

            "generated_by": item.generated_by,

            "generated_at": item.generated_at
        })


    return success_response(

        message="Forecast history fetched",

        data=data
    )

# Forecast Comparison
@router.get("/forecast-comparison")
@cache(expire=60)
def forecast_comparison(
    db: Session = Depends(get_db),
    user = Depends(verify_role("all"))
):

    forecasts = db.query(ForecastResult).all()

    data = []

    for item in forecasts:

        actual_sales = item.predicted_demand * 0.95

        difference = (item.predicted_demand - actual_sales)

        data.append({

            "forecast_date":
            item.forecast_date,

            "actual_sales":
            round(actual_sales,2),

            "predicted_sales":
            round(
                item.predicted_demand,2),

            "difference":
            round(difference,2)
        })


    return success_response(

        message="Forecast comparison analytics fetched",

        data=data
    )

# Model Comparison
@router.get("/model-comparison")
def model_comparison(

    db: Session = Depends(get_db),

    user = Depends(
        verify_role("all")
    )
):
    forecasts = (

        db.query(ForecastResult)

        .order_by(
            ForecastResult.forecast_date
        )

        .limit(30)

        .all()
    )
    if not forecasts:

        return success_response(

            message="No forecast data found",

            data=[]
        )
    comparison = []
    for row in forecasts:

        comparison.append({

            "date":
            str(row.forecast_date),

            "prophet":
            round(
                row.prophet_prediction or 0,
                2
            ),

            "linear_regression":
            round(
                row.lr_prediction or 0,
                2
            ),

            "moving_average":
            round(
                row.ma_prediction or 0,
                2
            ),

            "ensemble":
            round(
                row.predicted_demand or 0,
                2
            )
        })
    return success_response(

        message="Model comparison generated",

        data=comparison
    )        

#Model Accuracy
@router.get("/model-accuracy")
def model_accuracy(

    db: Session = Depends(get_db),

    user = Depends(
        verify_role("all")
    )
):
    accuracy_rows = (

    db.query(ForecastAccuracy)

    .order_by(
        ForecastAccuracy.evaluation_date
    )

    .limit(30)

    .all()
)
    if not accuracy_rows:

        return error_response(

            message="No accuracy data found",

            details=[]
    )
    accuracy_data = []
    for row in accuracy_rows:

        accuracy_data.append({

        "date":
        str(row.evaluation_date),

        "accuracy":
        round(
            row.accuracy_percentage,
            2
        )
        })
        
    current_accuracy = round(accuracy_rows[-1].accuracy_percentage,2)
    average_accuracy = round(

    sum(row.accuracy_percentage for row in accuracy_rows) /len(accuracy_rows),2)
    
    return success_response(

    message="Accuracy trends generated",

    data={

        "current_accuracy":
        current_accuracy,

        "average_accuracy":
        average_accuracy,

        "trend":
        accuracy_data
    }
)

@router.get("/forecast-confidence")
def get_forecast_confidence(
    db: Session = Depends(get_db),
    user = Depends(verify_role("all")
    )
):
    forecasts = (

    db.query(ForecastResult)

    .order_by(
        ForecastResult.forecast_date
    ).all()
)
    if not forecasts:

        return success_response(

        message="No forecast data found",

        data={}
    )
    avg_confidence = round(
    sum(row.confidence_score for row in forecasts)/len(forecasts),2)
    trend = []     
    for row in forecasts:

        trend.append({

        "date":
        str(row.forecast_date),

        "confidence":
        row.confidence_score
    })
    
    return success_response(

    message="Confidence score generated",

    data={

        "average_confidence":
        avg_confidence,

        "trend":
        trend
    }
)

