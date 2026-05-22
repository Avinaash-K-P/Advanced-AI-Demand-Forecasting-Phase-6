import pandas as pd
from prophet import Prophet
from app.db.session import SessionLocal
from app.models.user import User
from app.models.sales import Sales
from app.models.forecast import ForecastResult
from app.models.model_metadata import ModelMetadata
import pandas as pd
from datetime import datetime

def auto_generate_forecast():

    db = SessionLocal()

    try:

        print("Generating automatic forecast...")

        # Fetch sales data
        sales_data = db.query(Sales).all()
        data = []

        for row in sales_data:

            data.append({

                "ds": row.sales_date ,

                "y": row.quantity_sold
            })

        # Convert to dataframe
        df = pd.DataFrame(data)

        # Train model
        forecast = train_forecast_model(df, days = 0)

        # Clear old forecast data
        db.query(ForecastResult).delete()

        # Save new forecast
        for item in forecast.to_dict(orient="records"):

            new_forecast = ForecastResult(

                forecast_date=item["ds"],

                predicted_demand=item["predicted_demand"]
            )

            db.add(new_forecast)

        db.commit()

        # Metadata
         
        current_sales_count = db.query(Sales).count()    
        metadata = db.query(ModelMetadata).first()

        if not metadata:
            print("Initialising meta data....")
            metadata = ModelMetadata(last_sales_count=0)
            db.add(metadata)
            db.commit()
            db.refresh(metadata)

        elif current_sales_count > metadata.last_sales_count:
            print("New sales detected")
            metadata.last_sales_count = current_sales_count
            metadata.last_trained_at = datetime.utcnow()
            db.commit()    

    except Exception as e:

        print("AUTO FORECAST ERROR:", e)

    finally:

        db.close()    

    print("Forecast updated successfully!")

def preprocess_sales_data(df: pd.DataFrame):

    # Convert sales_date to datetime
    df["sales_date"] = pd.to_datetime(
        df["sales_date"]
    )

    # Group by date and sum quantity
    grouped_df = df.groupby(
        "sales_date"
    )["quantity_sold"].sum().reset_index()

    # Rename columns for Prophet
    grouped_df.columns = ["ds", "y"]

    # Sort by date
    grouped_df = grouped_df.sort_values("ds")

    return grouped_df

def train_forecast_model(df: pd.DataFrame, days: int):

    # Create Prophet model
    model = Prophet()

    # Train model
    model.fit(df)

    # Generate future dates

    future = model.make_future_dataframe(periods = days)

    # Predict future demand
    forecast = model.predict(future)

    # Select important columns
    result = forecast[[
        "ds",
        "yhat"
    ]].tail(30)

    # Rename prediction column
    result = result.rename(
        columns={
            "yhat": "predicted_demand"
        }
    )

    return result