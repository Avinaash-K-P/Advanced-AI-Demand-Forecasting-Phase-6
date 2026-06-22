from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import verify_role, get_current_user
from app.utils.response import success_response
from app.db.database import get_db
from app.models.user import User
from app.models.forecast_results import ForecastResult
from app.models.forecast_scenario import Scenario
from app.schemas.scenario import ScenarioCreate


router = APIRouter(prefix="/scenario", tags=["Forecast Scenario"])

# routes/scenario.py

@router.post(
    "/create-scenario"
)
def create_scenario(

    payload: ScenarioCreate,

    db: Session = Depends(get_db),

    user = Depends(verify_role("analyst")),

    current_user: User = Depends(get_current_user)

):
    new_scenario = Scenario(

    organization_id = current_user.organization_id,    

    scenario_name=
    payload.scenario_name,

    sales_growth_factor=
    payload.sales_growth_factor,

    seasonality_factor=
    payload.seasonality_factor,

    demand_factor=
    payload.demand_factor

)

    db.add(new_scenario)

    db.commit()

    db.refresh(new_scenario)

    return success_response(

    message="Scenario created",

    data=new_scenario

)

@router.get("/get-scenario")
def get_scenarios(
    db: Session = Depends(get_db),
    user = Depends(verify_role("analyst"))
):

    scenarios = db.query(
        Scenario
    ).all()

    return success_response(
        message="List of all Scenarios",
        data=scenarios
    )

@router.get(
    "/scenario/{scenario_id}/forecast"
)
def run_scenario_forecast(

    scenario_id:int,

    db:Session=Depends(get_db),

    user = Depends(verify_role("analyst"))

):
    scenario = db.query(
    Scenario
).filter(
    Scenario.id == scenario_id
).first()

    forecast_rows = db.query(
    ForecastResult
).all()
    
    results = []

    for row in forecast_rows:

        adjusted_demand = (

        row.predicted_demand

        * scenario.sales_growth_factor

        * scenario.seasonality_factor

        * scenario.demand_factor

    )

        results.append({

        "forecast_date":
        row.forecast_date,

        "original_demand":
        row.predicted_demand,

        "scenario_demand":
        round(adjusted_demand,2)

    })

    data = results

    return success_response(

    message="Scenario forecast generated",

    data=data

)

@router.get(
    "/compare"
)
def compare_scenarios(

    scenario1:int,

    scenario2:int,

    db:Session=Depends(get_db), 

    user = Depends(verify_role("analyst"))

):
    scenario_a = db.query(Scenario).get(scenario1)

    scenario_b = db.query(Scenario).get(scenario2)

    if scenario_a == scenario_b:

        raise HTTPException(

        status_code=400,

        detail="Select two different scenarios"

    )

    result = {
        "scenario1_name":
        scenario_a.scenario_name,

        "scenario2_name":
        scenario_b.scenario_name,

        "scenario1_growth":
        scenario_a.sales_growth_factor,

        "scenario2_growth":
        scenario_b.sales_growth_factor,

        "scenario1_demand":
        scenario_a.demand_factor,

        "scenario2_demand":
        scenario_b.demand_factor
    }

    return success_response(
        message = "comparison",
        data = result
    )