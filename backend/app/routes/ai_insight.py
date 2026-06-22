from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy import desc, func
from sqlalchemy.orm import Session
from app.core.security import verify_role, get_current_user
from app.db.database import get_db
from app.utils.response import success_response
from app.models.forecast_results import ForecastResult
from app.models.user import User
from app.models.sales import Sales

router = APIRouter(prefix="/ai-insights", tags=["AI Insights"])

@router.get("/recommendations")
def generate_recommendations(
    db: Session = Depends(get_db),
    user = Depends(verify_role("all"))
):
    forecast_rows = db.query(
    ForecastResult
).all()
    
    avg_demand = sum(
    row.predicted_demand
    for row in forecast_rows
) / len(forecast_rows)
    
    if avg_demand > 50:

        recommendation = (

        "Increase inventory to meet expected demand"

    )

    else:

        recommendation = (

        "Maintain current inventory levels"

    )
        
    return success_response(
    message = "recommendation generated",
    data={

        "recommendation":
        recommendation

    }

)

@router.get("/opportunities")
def get_opportunties(
    db: Session = Depends(get_db),
    user = Depends(verify_role("all"))
    ):
    
    top_products = (

    db.query(

        Sales.product_id,

        func.sum(
            Sales.quantity_sold
        ).label(
            "total_sales"
        )

    )

    .group_by(
        Sales.product_id
    )

    .order_by(
        desc(
            "total_sales"
        )
    )

    .limit(5)

    .all()

)
    opportunities = []

    for product in top_products:

        opportunities.append({

            "product_id":
            product.product_id,

            "total_sales":
            float(
                product.total_sales
            ),

            "opportunity":
            "High demand growth potential"

        })

        return success_response(

        message=
        "Demand opportunities identified",

        data=
        opportunities

    )    

@router.get("/declining-products")
def declining_products(
    db:Session = Depends(get_db),
    user = Depends(verify_role("all"))
    ):
    products = (

        db.query(
        Sales.product_id,
        func.sum(
            Sales.quantity_sold
        ).label(
            "total_sales"
        )
    )

    .group_by(
        Sales.product_id
    )

    .all()

)
    avg_sales = (

    sum( p.total_sales for p in products) // len(products) 
    
    )


    DECLINE_THRESHOLD = (avg_sales * Decimal(0.5))
    declining = []

    for product in products:

        if product.total_sales < DECLINE_THRESHOLD:

            declining.append({

                "product_id":
                product.product_id,

                "total_sales":
                float(
                    product.total_sales
                ),

                "warning":
                "Demand declining"

            })
    # for product in products:

    #     print(
    #     product.product_id,
    #     product.total_sales
    # )

    return success_response(

        message="Declining products detected",

        data=declining

    )        

@router.get(
    "/high-growth-products"
)
def high_growth_products(
    db: Session = Depends(get_db),
    user = Depends(verify_role("all"))
):   
    products = (

    db.query(

        Sales.product_id,

        func.sum(
            Sales.quantity_sold
        ).label(
            "total_sales"
        )

    )

    .group_by(
        Sales.product_id
    )

    .all()

)
    avg_sales = (

    sum( p.total_sales for p in products) / len(products) 
    
    )

    HIGH_GROWTH_THRESHOLD = (avg_sales * Decimal(1.5))
    growth_products = []
    
    for product in products:

        if product.total_sales > HIGH_GROWTH_THRESHOLD:

            growth_products.append({

            "product_id":
            product.product_id,

            "total_sales":
            float(
                product.total_sales
            ),

            "growth_status": "High Growth"

        })
    
    # for product in products:

    #     print(
    #     product.product_id,
    #     product.total_sales
    # )

    return success_response(

    message=
    "High growth products identified",

    data=growth_products
)


@router.get("/summary")
def forecast_summary(
    db: Session = Depends(get_db),
    user = Depends(verify_role("all"))
):

    forecast_rows = db.query(
        ForecastResult
    ).all()

    if not forecast_rows:

        return success_response(
            message="No forecast data available",
            data={
                "summary": "No forecast records found."
            }
        )

    avg_demand = (
        sum(
            row.predicted_demand
            for row in forecast_rows
        )
        /
        len(forecast_rows)
    )

    max_demand = max(
        row.predicted_demand
        for row in forecast_rows
    )

    summary = f"""
Forecast analysis indicates an average demand of {round(avg_demand, 2)} units.

Peak forecast demand is {round(max_demand, 2)} units.

Business demand is expected to remain stable.

Inventory planning is recommended.
"""

    return success_response(
        message="Forecast summary generated",
        data={
            "summary": summary
        }
    )