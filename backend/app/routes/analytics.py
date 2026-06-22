from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.database import get_db
from app.utils.response import success_response
from app.utils.pagination import paginator
from app.utils.logger import log_api_activity
from app.models.user import User
from app.models.sales import Sales
from app.models.forecast_results import ForecastResult
from app.models.forecast_history import ForecastHistory
from app.models.alerts import Alert
from app.models.api_logs import APILog
from sklearn.metrics import mean_absolute_error
from app.core.security import verify_role
import statistics
import time
from sqlalchemy import or_
from fastapi_cache.decorator import cache
from app.models.inventory import Inventory

router = APIRouter(prefix="/analytics", tags=["Analytics"])

# Global Search
@router.get("/global-search")
def global_search(

    query: str,

    db: Session = Depends(get_db),

    user = Depends(verify_role("all"))
):

    sales = db.query(Sales).filter(

        or_(

            Sales.product_name.ilike(f"%{query}%"),

            Sales.category.ilike(f"%{query}%"),

            Sales.region.ilike(f"%{query}%")
        )
    ).limit(20).all()


    users = db.query(User).filter(

        or_(

            User.username.ilike(f"%{query}%"),

            User.email.ilike(f"%{query}%")
        )
    ).all()


    forecast_history = db.query(

        ForecastHistory

    ).filter(

        ForecastHistory.model_type.ilike(
            f"%{query}%"
        )

    ).all()


    return success_response(

        message="Global search results",

        data={

            "sales": [

                {

                    "product":
                    item.product_name,

                    "category":
                    item.category,

                    "region":
                    item.region
                }

                for item in sales
            ],

            "users": [

                {

                    "username":
                    item.username,

                    "email":
                    item.email
                }

                for item in users
            ],

            "forecasts": [

                {

                    "model_type":
                    item.model_type,

                    "forecast_date":
                    item.forecast_date
                }

                for item in forecast_history
            ]
        }
    )


# Live Forecast
@router.get("/live-forecast")
def get_forecast(
    db: Session = Depends(get_db),
    user = Depends(verify_role("all"))
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

    log_api_activity(

        db=db,

        username= user["username"],

        endpoint="/live-forecast",

        method="GET",

        status="SUCCESS"
    )

    return success_response(

        message="Live forecast data fetched successfully",

        data=data
    )

# System performance
@router.get("/system-performance")
def system_performance(

    db: Session = Depends(get_db),

    user = Depends(verify_role("all"))
):
    start_time = time.time()

    total_users = db.query(User).count()

    total_sales = db.query(Sales).count()

    total_forecasts = db.query(ForecastHistory).count()

    total_api_logs = db.query(APILog).count()

    response_time = round(time.time() - start_time,4)

    data = {

        "total_users": total_users,

        "total_sales_records": total_sales,

        "total_forecasts_generated":
        total_forecasts,

        "total_api_requests":
        total_api_logs,

        "api_response_time_seconds":
        response_time
    }

    return success_response(

        message="System performance metrics fetched",

        data=data
    ) 

# Sales Data
@router.get("/recent-sales")
def recent_sales(

    db: Session = Depends(get_db),

    user = Depends(verify_role("all"))
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


# Seasonal Trends
@router.get("/seasonal-trends")
def seasonal_trends(

    db: Session = Depends(get_db),

    user = Depends(verify_role("all"))
):

    forecasts = db.query(
        ForecastResult
    ).order_by(

        ForecastResult.forecast_date.asc()

    ).all()


    data = []

    for item in forecasts:

        data.append({

            "forecast_date": item.forecast_date,

            "predicted_demand": item.predicted_demand,

            "sales_trend": item.sales_trend,

            "weekly_pattern": item.weekly_pattern,

            "yearly_pattern": item.yearly_pattern
        })


    return success_response(

        message="Seasonal trend data fetched successfully",

        data=data
    )

# Anomaly Detection
@router.get("/detect-anomalies")
def detect_anomalies(

    db: Session = Depends(get_db),

    user = Depends(verify_role("all"))
):

    sales = db.query(Sales).all()

    quantities = [

        item.quantity_sold

        for item in sales
    ]

    mean_value = statistics.mean(
        quantities
    )


    std_value = statistics.stdev(
        quantities
    )

    upper_limit = mean_value + (2 * std_value)

    lower_limit = mean_value - (2 * std_value)

    anomalies = []


    for item in sales:

        if (

            item.quantity_sold > upper_limit

            or

            item.quantity_sold < lower_limit
        ):

            anomalies.append({

                "product_name": item.product_name,

                "region": item.region,

                "quantity_sold": item.quantity_sold,

                "date": item.sales_date,

                "status": "Anomaly Detected"
            })


    return success_response(

        message="Anomaly detection completed",

        data={

            "mean": mean_value,

            "standard_deviation": std_value,

            "anomalies": anomalies
        }
    )

# Region wise analytics
@router.get("/region-forecast")
@cache(expire=60)
def region_forecast(

    db: Session = Depends(get_db),

    user = Depends(verify_role("all"))
):

    sales = db.query(Sales).all()


    region_data = {}


    for item in sales:

        if item.region not in region_data:

            region_data[item.region] = 0


        region_data[item.region] += item.quantity_sold


    data = []


    for region, total in region_data.items():

        data.append({

            "region": region,

            "forecasted_demand": total
        })

    #print("This will not display if cache worked !!")
    
    return success_response(

        message="Region-wise forecast analytics fetched",

        data=data
    )

# Catagory wise analytics
@router.get("/category-sales")
@cache(expire=60)
def category_sales(

    db: Session = Depends(get_db),

    user = Depends(verify_role("all"))
):

    sales = db.query(Sales).all()


    category_data = {}


    for item in sales:

        if item.category not in category_data:

            category_data[item.category] = 0


        category_data[item.category] += item.quantity_sold


    data = []


    for category, total in category_data.items():

        data.append({

            "category": category,

            "total_sales": total
        })


    return success_response(

        message="Category-wise sales analytics fetched",

        data=data
    )

# Revenue Prediction
@router.get("/revenue-prediction")
@cache(expire=60)
def revenue_prediction(

    db: Session = Depends(get_db),

    user = Depends(verify_role("all"))
):

    forecasts = db.query(
        ForecastResult
    ).all()


    data = []


    for item in forecasts:

        predicted_revenue = (

            item.predicted_demand * 100
        )


        data.append({

            "forecast_date": item.forecast_date,

            "predicted_revenue": predicted_revenue
        })


    return success_response(

        message="Revenue prediction analytics fetched",

        data=data
    )

# Inventory risk analytics
@router.get("/inventory-risk")
@cache(expire=60)
def inventory_risk(

    db: Session = Depends(get_db),

    user = Depends(verify_role("all"))
):

    sales = db.query(Sales).all()


    data = []


    for item in sales:

        predicted_demand = (

            item.quantity_sold * 1.2
        )


        if item.stock_available < predicted_demand:

            risk = "High Risk"


        elif item.stock_available <= (

            predicted_demand * 1.5
        ):

            risk = "Medium Risk"


        else:

            risk = "Low Risk"


        data.append({

            "product": item.product_name,

            "stock_available": item.stock_available,

            "predicted_demand": predicted_demand,

            "risk_level": risk
        })


    return success_response(

        message="Inventory risk analysis fetched",

        data=data
    )

# Total Sales and Quantity
@router.get("/total-sales")
@cache(expire=60)
def get_total_sales(
    start_date: str = None,
    end_date: str = None,
    category: str = None,
    region: str = None,
    db: Session = Depends(get_db),
    user = Depends(verify_role("all"))
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
    user = Depends(verify_role("all"))
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
    user = Depends(verify_role("all"))
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
@cache(expire=60)
def get_forecast_accuracy(
    db: Session = Depends(get_db),
    user = Depends(verify_role("all"))
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
            data = {"accuracy":"N/A"
                    }
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
            "compared_dates": len(common_dates),
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
    user = Depends(verify_role("all"))
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

#Alert display
@router.get("/get-alert")
def get_alerts(
    db:Session = Depends(get_db),
    user = Depends(verify_role("all"))
):

    alerts = db.query(Alert).order_by(Alert.created_at.desc()).all()

    return success_response(
        message="Alert generated",
        data=alerts
    )

# Customer behaviour
@router.get("/customer-behavior")
def customer_behavior_analysis(

    db: Session = Depends(get_db),

    user = Depends(
        verify_role("all")
    )
):
    total_customers = db.query(

        func.count(
            func.distinct(
                Sales.customer_id
            )
        )

    ).scalar()   

    repeat_customers = db.query(

        Sales.customer_id

    ).group_by(

        Sales.customer_id

    ).having(

        func.count(
            Sales.transaction_id
        ) > 1

    ).count()

    top_segment = db.query(

        Sales.customer_segment,

        func.count(
            Sales.customer_segment
        )

    ).group_by(

        Sales.customer_segment

    ).order_by(

        func.count(
            Sales.customer_segment
        ).desc()

    ).first()

    top_gender = db.query(

        Sales.customer_gender,

        func.count(
            Sales.customer_gender
        )

    ).group_by(

        Sales.customer_gender

    ).order_by(

        func.count(
            Sales.customer_gender
        ).desc()

    ).first()

    top_age_group = db.query(

        Sales.customer_age,

        func.count(
            Sales.customer_age
        )

    ).group_by(

        Sales.customer_age

    ).order_by(

        func.count(
            Sales.customer_age
        ).desc()

    ).first()

    return success_response(

        message="Customer behavior analysis completed",

        data={

            "total_customers":
            total_customers,

            "repeat_customers":
            repeat_customers,

            "top_segment":
            top_segment[0]
            if top_segment
            else None,

            "top_gender":
            top_gender[0]
            if top_gender
            else None,

            "top_age_group":
            top_age_group[0]
            if top_age_group
            else None
        }
    )

@router.get(
    "/business-recommendations"
)
def get_business_recommendations(
    db: Session = Depends(get_db),
        user = Depends(verify_role("all"))
):
    forecasts = (

    db.query(
        ForecastResult
    )

    .order_by(
        ForecastResult.forecast_date
    )

    .all()
)
    if not forecasts:

        return success_response(

        message="No forecast data found",

        data=[]
    )
    avg_demand = sum(row.predicted_demand for row in forecasts) / len(forecasts)

    avg_confidence = sum(row.confidence_score for row in forecasts) / len(forecasts)

    latest_trend = forecasts[-1].sales_trend
    
    recommendations = []
    
    if avg_demand > 25:

        recommendations.append({

        "type":
        "Inventory",

        "priority":
        "High",

        "message":
        "Increase inventory levels due to strong demand forecasts."
    })
        
    if latest_trend > 0:

        recommendations.append({

        "type":
        "Sales",

        "priority":
        "Medium",

        "message":
        "Demand trend is increasing. Prepare for higher order volume."
    })

    if avg_confidence < 75:

        recommendations.append({

        "type":
        "Forecast",

        "priority":
        "High",

        "message":
        "Forecast confidence is low. Review forecasting inputs."
    })    
        
    if avg_confidence >= 90:

        recommendations.append({

        "type":
        "Forecast",

        "priority":
        "Low",

        "message":
        "Forecast confidence is high. Current planning assumptions look reliable."
    })

    return success_response(

    message="Recommendations generated",

    data=recommendations
    )