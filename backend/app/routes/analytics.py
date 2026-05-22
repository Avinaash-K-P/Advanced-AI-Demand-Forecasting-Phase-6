from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.database import get_db
from app.utils.response import success_response
from app.utils.pagination import paginator
from app.models.sales import Sales
from app.models.forecast import ForecastResult
from sklearn.metrics import mean_absolute_error
from app.core.security import verify_token


router = APIRouter(prefix="/analytics", tags=["analytics"])

# Live Forecast
@router.get("/live-forecast")
def get_forecast(
    db: Session = Depends(get_db),
    user = Depends(verify_token)
):

    forecasts = db.query(
        ForecastResult
    ).order_by(

        ForecastResult.forecast_date.desc()

    ).limit(10).all()


    data = []

    for item in forecasts:

        data.append({

            "forecast_date": item.forecast_date,

            "predicted_demand": item.predicted_demand
        })


    return success_response(

        message="Live forecast data fetched successfully",

        data=data
    )

# Sales Data
@router.get("/recent-sales")
def recent_sales(

    db: Session = Depends(get_db),

    user = Depends(verify_token)
):

    sales = db.query(Sales).order_by(

        Sales.id.desc()

    ).limit(10).all()


    data = []

    for item in sales:

        data.append({

            "product_name": item.product_name,

            "category": item.category,

            "region": item.region,

            "quantity_sold": item.quantity_sold,

            "revenue": item.revenue,

            "date": item.sales_date
        })


    return success_response(

        message="Recent sales fetched successfully",

        data=data
    )

# Total Sales and Quantity
@router.get("/total-sales")
def get_total_sales(
    start_date: str = None,
    end_date: str = None,
    category: str = None,
    region: str = None,
    db: Session = Depends(get_db),
    user = Depends(verify_token)
):
    query = db.query(Sales)

    if start_date:
        query = query.filter(Sales.sales_date >= start_date)

    if end_date:
        query = query.filter(Sales.sales_date <= end_date)    

    if category:
        query = query.filter(Sales.category == category)

    if region:
        query = query.filter(Sales.region == region)

    total_sales = query.with_entities(
        func.sum(Sales.revenue)
    ).scalar()

    total_quantity = query.with_entities(
        func.sum(Sales.quantity_sold)
    ).scalar()

    data =  {
            "total_revenue": total_sales or 0,
            "total_quantity_sold": total_quantity or 0
        }

    return success_response(
    message = "Total sales and quantity retrieved successfully!",
    data =  data
    )    

# Monthly Sales Trend
@router.get("/monthly-sales")
def get_monthly_sales(
    start_date: str = None,
    end_date: str = None,
    category: str = None,
    region: str = None,
    db: Session = Depends(get_db),
    user = Depends(verify_token)
):
    query = db.query(Sales)

    if start_date:
        query = query.filter(Sales.sales_date >= start_date)

    if end_date:
        query = query.filter(Sales.sales_date <= end_date)    

    if category:
        query = query.filter(Sales.category == category)

    if region:
        query = query.filter(Sales.region == region)


    results = query.with_entities(func.date_format(Sales.sales_date,"%Y-%m").label("month"),

        func.sum(Sales.revenue).label(
            "total_revenue")

    ).group_by("month").all()


    data = []

    for row in results:

        data.append({
            "month": row.month,
            "total_revenue": float(
                row.total_revenue
            )
        })

    return success_response(
        message = "Monthly sales trend retrieved successfully!",
        data = data
    )

# Forecast Results
@router.get("/forecast-results")
def get_forecast_results(
    skip:int = None,
    limit:int = None,
    start_date: str = None,
    end_date: str = None,
    db: Session = Depends(get_db),
    user = Depends(verify_token)
):

    query = db.query(ForecastResult)
    
    if start_date:
        query = query.filter(ForecastResult.forecast_date >= start_date)

    if end_date:
        query = query.filter(ForecastResult.forecast_date <= end_date)

    data = paginator(query,skip,limit)
    return success_response(
        message = "Forecast results retrieved successfully!",
        data = data
    )

# Forecast Accuracy
@router.get("/forecast-accuracy")
def get_forecast_accuracy(
    db: Session = Depends(get_db),
    user = Depends(verify_token)
):

    sales_data = db.query(Sales).all()

    forecast_data = db.query(
        ForecastResult
    ).all()

    # Convert actual sales
    actual_dict = {}

    for row in sales_data:

        date_key = str(row.sales_date)

        if date_key not in actual_dict:
            actual_dict[date_key] = 0

        actual_dict[date_key] += row.quantity_sold

    # Convert forecast data
    predicted_dict = {}

    for row in forecast_data:

        date_key = str(row.forecast_date)

        predicted_dict[date_key] = (
            row.predicted_demand
        )

    # Find common dates
    common_dates = set(
        actual_dict.keys()
    ).intersection(
        predicted_dict.keys()
    )

    if not common_dates:

        return success_response(
            message = "No matching dates found for accuracy calculation",
            data = {}
        )

    actual_values = []
    predicted_values = []

    for date in common_dates:

        actual_values.append(
            actual_dict[date]
        )

        predicted_values.append(
            predicted_dict[date]
        )

    # Calculate MAE
    mae = mean_absolute_error(
        actual_values,
        predicted_values
    )

    # Simple interpretation
    if mae < 5:
        performance = "Excellent"

    elif mae < 15:
        performance = "Good"

    else:
        performance = "Needs Improvement"

    return success_response(
        message = "Forecast accuracy calculated successfully!",
        data =  {
            "mae": round(mae, 2),
            "model_performance": performance,
            "compared_dates": len(common_dates)
        }
    )

# Top Selling Products
@router.get("/top-products")
def get_top_products(
    start_date: str = None,
    end_date: str = None,
    category: str = None,
    region: str = None,
    db: Session = Depends(get_db),
    user = Depends(verify_token)
):
    query = db.query(Sales)

    if start_date:
        query = query.filter(Sales.sales_date >= start_date)

    if end_date:
        query = query.filter(Sales.sales_date <= end_date)    

    if category:
        query = query.filter(Sales.category == category)

    if region:
        query = query.filter(Sales.region == region)


    results = query.with_entities(
        Sales.product_name,
        func.sum(Sales.quantity_sold).label("total_quantity")
    ).group_by(Sales.product_name).order_by(func.sum(Sales.quantity_sold).desc()).limit(5).all()

    data = []

    for row in results:
        data.append({
            "product_name": row.product_name,
            "total_quantity_sold": int(row.total_quantity),
        })

    return success_response(
        message = "Top selling products retrieved successfully!",
        data = data
    )
