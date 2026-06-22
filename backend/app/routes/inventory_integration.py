from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.Inventory_Integration import InventoryIntegration
from app.models.inventory import Inventory
from app.schemas.Inventory_integration import InventoryIntegrationCreate
from app.services.integration_service import call_external_api
from app.core.security import verify_role
from app.utils.response import success_response, error_response
from datetime import datetime
from app.models.forecast_results import ForecastResult

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory Integration"]
)

@router.post("/save")
def save_inventory_integration(

    integration: InventoryIntegrationCreate,

    db: Session = Depends(get_db),

    user = Depends(
        verify_role("admins")
    )
):

    new_integration = InventoryIntegration(

        system_name=integration.system_name,

        api_url=integration.api_url,

        api_key=integration.api_key
    )

    db.add(new_integration)

    db.commit()

    db.refresh(new_integration)

    return success_response(

        message="Inventory integration saved successfully!",

        data={

            "id": new_integration.id,

            "system_name": new_integration.system_name
        }
    )

@router.post("/test-connection")
def test_inventory_connection(

    integration: InventoryIntegrationCreate,

    user = Depends(
        verify_role("admins")
    )
):

    try:

        result = call_external_api(

             integration.api_url
        )

        if result.status_code == 200:

            return success_response(

                message="Connection successful!",

                data={

                    "status": "Connected"
                }
            )

        return error_response(

            message="Connection failed!",

            details={

                "status": "Failed"
            }
        )

    except Exception as e:

        return error_response(

            message="Connection failed!",

            details={

                "status": str(e)
            }
        )
    
@router.post("/sync")
def sync_inventory(

    db: Session = Depends(get_db),

    user = Depends(
        verify_role("admins")
    )
):

    try:

        integration = db.query(
            InventoryIntegration
        ).filter(
            InventoryIntegration.is_active == True
        ).first()

        if not integration:

            return error_response(

                message="No active inventory integration found!",

                details={}
            )

        result = call_external_api(

            integration.api_url
        )

        if result.status_code != 200:

            return error_response(

                message="Inventory sync failed!",

                details={}
            )

        # To clear the old data
        db.query(Inventory).delete()
        
        inventory_data = result.json()

        synced_count = 0

        for item in inventory_data[:20]:

            inventory = Inventory(

                product_name=item.get(
                    "title",
                    "Unknown Product"
                ),

                stock_quantity=100,

                source_system=integration.system_name,

                synced_at=datetime.utcnow()
            )

            db.add(inventory)

            synced_count += 1

        integration.last_sync = (
            datetime.utcnow()
        )

        db.commit()

        return success_response(

            message="Inventory synced successfully!",

            data={

                "records_synced":
                synced_count
            }
        )

    except Exception as e:

        return error_response(

            message="Inventory sync failed!",

            details={

                "error": str(e)
            }
        )    
    
@router.get("/all")
def get_integrations(

    db: Session = Depends(get_db),

    user = Depends(
        verify_role("admins")
    )
):

    integrations = db.query(
        InventoryIntegration
    ).all()

    return success_response(

        message="Integrations fetched successfully",

        data=integrations
    )

@router.put("/{id}/toggle")
def toggle_integration(

    id: int,

    db: Session = Depends(get_db),

    user = Depends(
        verify_role("admins")
    )
):

    integration = db.query(
        InventoryIntegration
    ).filter(
        InventoryIntegration.id == id
    ).first()

    if not integration:

        raise HTTPException(
            status_code=404,
            detail="Integration not found"
        )

    integration.is_active = (
        not integration.is_active
    )

    db.commit()

    return success_response(

        message="Integration updated",

        data={
            "active":
            integration.is_active
        }
    )

@router.post("/webhook/inventory-update")
def inventory_webhook(

    payload: dict,

    db: Session = Depends(get_db),
      user = Depends(verify_role("admins"))
):

    product = payload.get(
        "product_name"
    )

    quantity = payload.get(
        "stock_quantity"
    )

    inventory = Inventory(

        product_name=product,

        stock_quantity=quantity,

        source_system="Webhook",

        synced_at=datetime.utcnow()
    )

    db.add(inventory)

    db.commit()

    return success_response(

        message="Webhook processed successfully",

        data={}
    )

#Low stock prediction system
@router.get("/global-stock-risk")
def global_stock_risk(

    db: Session = Depends(get_db),

    user = Depends(
        verify_role("all")
    )
):
    inventory = db.query(Inventory).all()

    forecasts = db.query(ForecastResult).all()

    total_stock = sum(

    item.stock_quantity or 0

    for item in inventory
    )
    average_demand = 0

    if forecasts:

        average_demand = (

        sum(
            item.predicted_demand
            for item in forecasts
        )

        /

        len(forecasts)
    )
        
    projected_demand = (average_demand * 100)    

    remaining_stock = (total_stock-projected_demand)

    if remaining_stock < 50:

        risk = "High"

    elif remaining_stock < 200:

        risk = "Medium"

    else:

        risk = "Low"

    return success_response(

        message="Global stock risk calculated",

        data={

        "total_stock":
        total_stock,

        "projected_demand":
        round(
            projected_demand,
            2
        ),

        "remaining_stock":
        round(
            remaining_stock,
            2
        ),

        "risk":
        risk
        }
    )     

# Demand Spike Prediction
@router.get("/demand-spikes")
def get_demand_spikes(

    db: Session = Depends(get_db),

    user = Depends(
        verify_role("all")
    )
):

    forecasts = db.query(
        ForecastResult
    ).all()

    if not forecasts:

        return success_response(

            message="No forecast data available",

            data=[]
        )

    average_demand = (
        sum(
            row.predicted_demand
            for row in forecasts
    )
        /  len(forecasts)
    )    

    spikes = []
    for row in forecasts:

        spike_percentage = ( (row.predicted_demand-average_demand) / average_demand ) * 100

        if spike_percentage > 10:

            severity = "High"

        elif spike_percentage > 5:

            severity = "Medium"

        else:

            continue

    spikes.append({

            "forecast_date":
            row.forecast_date,

            "predicted_demand":
            round(
                row.predicted_demand,
                2
            ),

            "spike_percentage":
            round(
                spike_percentage,
                2
            ),

            "severity":
            severity
    })   

    return success_response(

        message="Demand spike analysis completed",

        data=spikes
    )

# Demand Recommendation
@router.get("/demand")
def demand_recommendations(

    db: Session = Depends(get_db),

    user = Depends(
        verify_role("all")
    )
):

    forecasts = db.query(
        ForecastResult
    ).all()

    if not forecasts:

        return success_response(

            message="No forecast data found",

            data=[]
        )
    
    average_demand = (

        sum( row.predicted_demand for row in forecasts) / len(forecasts) 
    )
    
    recommendations = []
    for row in forecasts:
        demand = row.predicted_demand
        
        if demand > average_demand * 1.15:

            action = "Increase Inventory"

        elif demand < average_demand * 0.85:

            action = "Reduce Inventory"

        else:
            action = "Maintain Inventory"

        recommendations.append({

            "forecast_date":
            row.forecast_date,

            "predicted_demand":
            round(demand,2),

            "recommendation":
            action
        })    

    return success_response(

        message="Demand recommendations generated",

        data=recommendations
    )    

# Inventory Optimization
@router.get("/inventory-optimization")
def inventory_optimization(
  db: Session = Depends(get_db),
    user = Depends(
        verify_role("all")
    )
):    
   
    inventory = db.query(Inventory).all()
    forecasts = db.query(ForecastResult).all()
    if not inventory or not forecasts:

        return error_response(

        message="No data available",

        details=[]
    )
    
    total_stock = sum( item.stock_quantity or 0 for item in inventory )
    
    average_demand = (
        sum(row.predicted_demand for row in forecasts) / len(forecasts)
    )

    projected_demand = (average_demand * 100)

    if total_stock < projected_demand:

        suggestion = "Order More Inventory"

    elif total_stock > projected_demand * 2:

        suggestion = "Reduce Purchasing"

    else:

        suggestion = "Maintain Current Inventory"

    return success_response(

    message="Inventory optimization completed",

    data={

        "total_stock":
        total_stock,

        "projected_demand":
        round(
            projected_demand,
            2
        ),

        "suggestion":
        suggestion
    }
)    