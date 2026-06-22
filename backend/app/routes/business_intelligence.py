from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.core.security import verify_role
from app.db.database import get_db
from app.utils.response import success_response
from app.models.sales import Sales
from app.models.forecast_results import ForecastResult

router = APIRouter(prefix="/business", tags=["Business Intelligence"])

@router.get("/revenue-forecast")
def revenue_forecast(
    db: Session = Depends(get_db),
    user = Depends(verify_role("all"))
):
    sales_rows = db.query(
    Sales
).all()

    total_revenue = sum(
    float(row.revenue or 0)
    for row in sales_rows
)

    total_quantity = sum(
    float(row.quantity_sold or 0)
    for row in sales_rows
)

    avg_revenue_per_unit = (
    total_revenue / total_quantity
    if total_quantity > 0
    else 0
)
    
    forecast_rows = db.query(
    ForecastResult
).all()

    results = []

    for row in forecast_rows:

        revenue_forecast = (

        row.predicted_demand

        * avg_revenue_per_unit

    )

    results.append({

        "forecast_date":
        row.forecast_date,

        "predicted_demand":
        row.predicted_demand,

        "forecasted_revenue":
        round(
            revenue_forecast,
            2
        )

    })

    return success_response(

    message="Revenue forecast generated",

    data=results

)    

@router.get("/profit-forecast")
def profit_forecast(
    db: Session = Depends(get_db),
    user = Depends(verify_role("all"))
):
    PROFIT_MARGIN = 0.30

    sales_rows = db.query(
    Sales
).all()

    total_revenue = sum(
    float(row.revenue or 0)
    for row in sales_rows
)

    total_quantity = sum(
    float(row.quantity_sold or 0)
    for row in sales_rows
)

    avg_revenue_per_unit = (
    total_revenue / total_quantity
    if total_quantity > 0
    else 0
)

    forecast_rows = db.query(
    ForecastResult
    ).all()

    results = []

    for row in forecast_rows:

        revenue = (

        row.predicted_demand

        * avg_revenue_per_unit

    )

        profit = (

        revenue

        * PROFIT_MARGIN

    )

        results.append({

        "forecast_date":
        row.forecast_date,

        "forecasted_profit":
        round(
            profit,
            2
        )

    })
        
    return success_response(
        message="Profit Forecast",
        data = results
    )    
        
@router.get("/cost-analysis")
def cost_analysis(
    db: Session = Depends(get_db),
    user = Depends(verify_role("all"))
):
    sales_rows = db.query(
    Sales
).all()

    total_revenue = sum(
    float(row.revenue or 0)
    for row in sales_rows
)

    total_quantity = sum(
    float(row.quantity_sold or 0)
    for row in sales_rows
)

    avg_revenue_per_unit = (
    total_revenue / total_quantity
    if total_quantity > 0
    else 0
)
    
    forecast_rows = db.query(
    ForecastResult
).all()

    results = []
    
    forecast_total_revenue = 0

    forecast_total_profit = 0

    for row in forecast_rows:

        revenue = (

        row.predicted_demand

        * avg_revenue_per_unit

    )

        profit = revenue * 0.30

        forecast_total_revenue += revenue

        forecast_total_profit += profit

    results = {

        "forecasted_revenue":
        round(
            forecast_total_revenue,
            2
        ),

        "forecasted_profit":
        round(
            forecast_total_profit,
            2
        ),

        "forecasted_cost":
        round(

            forecast_total_revenue
            -
            forecast_total_profit,

            2

        )

    }
    return success_response(
    message = "Cost Analysis Details",    
    data= results
)

@router.get("/kpis")
def business_kpis(
    db: Session = Depends(get_db),
    user = Depends(verify_role("all"))
):
    
    total_sales = db.query(
    Sales
).count()
    total_forecasts = db.query(
    ForecastResult
).count()
    average_demand = db.query(
    func.avg(
        ForecastResult.predicted_demand
    )

).scalar()
    total_revenue = db.query(

    func.sum(
        Sales.revenue
    )

).scalar()

    return success_response(
    message = "KPI details",    
    data={

        "total_sales":
        total_sales,

        "total_forecasts":
        total_forecasts,

        "average_demand":
        round(
            average_demand or 0,
            2
        ),

        "total_revenue":
        round(
            total_revenue or 0,
            2
        )

    }

)

@router.get("/growth-impact")
def growth_impact(
    db: Session = Depends(get_db),
    user = Depends(verify_role("all"))
):
    
    current_revenue = db.query(

    func.sum(
        Sales.revenue
    )

).scalar() or 0
    
    forecast_revenue = 0

    sales_rows = db.query(
    Sales
).all()

    total_revenue = sum(
    float(row.revenue or 0)
    for row in sales_rows
)

    total_quantity = sum(
    float(row.quantity_sold or 0)
    for row in sales_rows
)

    avg_revenue_per_unit = (
    total_revenue / total_quantity
    if total_quantity > 0
    else 0
)
    
    forecast_rows = db.query(
    ForecastResult
).all()

    for row in forecast_rows:

        forecast_revenue += (

        row.predicted_demand

        * avg_revenue_per_unit

    )
    
    growth_percentage = (

    (
        forecast_revenue
        -
        current_revenue
    )

    /

    current_revenue

) * 100 if current_revenue > 0 else 0
    
    return success_response(
    message = "Growth Impact Details",        
    data={

        "current_revenue":
        round(
            current_revenue,
            2
        ),

        "forecast_revenue":
        round(
            forecast_revenue,
            2
        ),

        "growth_percentage":
        round(
            growth_percentage,
            2
        )

    }

)

@router.get("/executive-dashboard")
def excutive_dashboard(
    db: Session = Depends(get_db),
    user = Depends(verify_role("all"))
                       
):  
    rf = revenue_forecast(db)
    pf = profit_forecast(db)
    ca = cost_analysis(db)
    bk = business_kpis(db)
    gi = growth_impact(db)

    result = {"Revenue forecast" : rf["data"],
              "Cost Analysis" : ca["data"],
              "Business KPI's": bk["data"],
              "Growth Impact": gi["data"],
              "Profit Forecast" : pf["data"]
              }

    return success_response(
        message="Executive Dashboard",
        data = result
    )
    