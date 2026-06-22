from app.db.session import SessionLocal

from app.models.annual_plans import AnnualPlans
from app.models.quarterly_plans import QuarterlyPlans
from app.models.business_targets import BusinessTargets
from app.models.forecast_results import ForecastResult

from app.schemas.strategic_planning import (
    AnnualPlanCreate,
    AnnualPlanUpdate,
    QuarterlyPlanCreate,
    QuarterlyPlanUpdate,
    BusinessTargetCreate,
    BusinessTargetUpdate
)

from app.utils.response import (
    success_response,
    error_response
)

def create_annual_plan(
    plan_data: AnnualPlanCreate
):

    db = SessionLocal()

    try:

        plan = AnnualPlans(
            organization_id=plan_data.organization_id,
            year=plan_data.year,
            name=plan_data.name,
            description=plan_data.description,
            status=plan_data.status,
            created_by=plan_data.created_by
        )

        db.add(plan)
        db.commit()
        db.refresh(plan)

        return success_response(
            message="Annual plan created successfully",
            data={"annual_plan_id": plan.id}
        )

    except Exception as e:

        db.rollback()

        return error_response(
            message="Failed to create annual plan",
            details=str(e)
        )

    finally:

        db.close()

def update_annual_plan(
    plan_id: int,
    plan_data: AnnualPlanUpdate
):

    db = SessionLocal()

    try:

        plan = (
            db.query(AnnualPlans)
            .filter(AnnualPlans.id == plan_id)
            .first()
        )

        if not plan:

            return error_response(
                message="Annual plan not found"
            )

        update_data = plan_data.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():

            setattr(plan, field, value)

        db.commit()

        return success_response(
            message="Annual plan updated successfully"
        )

    except Exception as e:

        db.rollback()

        return error_response(
            message="Failed to update annual plan",
            details=str(e)
        )

    finally:

        db.close()

def create_quarterly_plan(
    plan_data: QuarterlyPlanCreate
):

    db = SessionLocal()

    try:

        plan = QuarterlyPlans(
            organization_id=plan_data.organization_id,
            annual_plan_id=plan_data.annual_plan_id,
            quarter=plan_data.quarter,
            year=plan_data.year,
            name=plan_data.name,
            description=plan_data.description,
            status=plan_data.status
        )

        db.add(plan)
        db.commit()
        db.refresh(plan)

        return success_response(
            message="Quarterly plan created successfully",
            data={"quarterly_plan_id": plan.id}
        )

    except Exception as e:

        db.rollback()

        return error_response(
            message="Failed to create quarterly plan",
            details=str(e)
        )

    finally:

        db.close()

def update_quarterly_plan(
    plan_id: int,
    plan_data: QuarterlyPlanUpdate
):                        
    
    db = SessionLocal()

    try:

        plan = (
            db.query(QuarterlyPlans)
            .filter(QuarterlyPlans.id == plan_id)
            .first()
        )

        if not plan:

            return error_response(
                message="Quarterly plan not found"
            )

        update_data = plan_data.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():

            setattr(plan, field, value)

        db.commit()

        return success_response(
            message="Quarterly plan updated successfully"
        )

    except Exception as e:

        db.rollback()

        return error_response(
            message="Failed to update quarterly plan",
            details=str(e)
        )

    finally:

        db.close()

def create_business_target(
    target_data: BusinessTargetCreate
):

    db = SessionLocal()

    try:

        target = BusinessTargets(
            organization_id=target_data.organization_id,
            annual_plan_id=target_data.annual_plan_id,
            quarterly_plan_id=target_data.quarterly_plan_id,
            target_name=target_data.target_name,
            target_type=target_data.target_type,
            target_value=target_data.target_value,
            current_value=target_data.current_value,
            unit=target_data.unit,
            status=target_data.status
        )

        db.add(target)
        db.commit()
        db.refresh(target)

        return success_response(
            message="Business target created successfully",
            data={"target_id": target.id}
        )

    except Exception as e:

        db.rollback()

        return error_response(
            message="Failed to create business target",
            details=str(e)
        )

    finally:

        db.close()        

def update_business_target(
    target_id: int,
    target_data: BusinessTargetUpdate
):        
    db = SessionLocal()

    try:

        plan = (
            db.query(BusinessTargets)
            .filter(BusinessTargets.id == target_id)
            .first()
        )

        if not plan:

            return error_response(
                message="Business target not found"
            )

        update_data = target_data.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():

            setattr(plan, field, value)

        db.commit()

        return success_response(
            message="Business target updated successfully"
        )

    except Exception as e:

        db.rollback()

        return error_response(
            message="Failed to business target",
            details=str(e)
        )

    finally:

        db.close()

def get_annual_dashboard(
    org_id: int
):  
    db = SessionLocal()

    annual_plans = db.query(AnnualPlans).filter(
        AnnualPlans.organization_id == org_id
        ).all()

    targets = db.query(BusinessTargets).filter(
        BusinessTargets.organization_id == org_id
        ).all()

    forecast_count = db.query(ForecastResult).filter(
        ForecastResult.organization_id == org_id
        ).count()        
    
    return success_response(
        message="Annual dashboard retrieved successfully",
        data={
        "annual_plans": annual_plans,
        "business_targets": targets,
        "forecast_count": forecast_count
    }
)
    
def get_quarterly_dashboard(
    org_id: int
):
    db = SessionLocal()

    quarterly_plans = db.query(QuarterlyPlans).filter(
        QuarterlyPlans.organization_id == org_id
        ).first()
    
    targets = db.query(BusinessTargets).filter(
        BusinessTargets.organization_id == org_id
        ).first()

    return success_response(
        message = "Quarterly dasboard retrieved successfully",
        data = {
            "quarterly_plans": quarterly_plans,
            "business_targets": targets
        }   
    )
    
def compare_forecast_vs_target(
    org_id: int
):

    db = SessionLocal()

    targets = db.query(BusinessTargets).filter(
        BusinessTargets.organization_id == org_id
    ).all()
    

    total_target = sum(
        target.target_value
        for target in targets
    )

    forecasts = db.query(ForecastResult).filter(
        ForecastResult.organization_id == org_id
    ).all()   

    total_forecast = sum(
        forecast.predicted_demand
        for forecast in forecasts
    )   

    variance = total_forecast - total_target

    return success_response(
        message= "Forecast and Target comparison fetched!!",
        data = {
                "target": total_target,
                "forecast": total_forecast,
                "variance": variance
        }        
    )

def generate_planning_recommendations(
    org_id: int
):
    db = SessionLocal()

    forecasts = db.query(ForecastResult).filter(
        ForecastResult.organization_id == org_id
        ).all()  

    targets = db.query(BusinessTargets).filter(
        BusinessTargets.organization_id == org_id
        ).all()
    
    forecast = sum(
    forecast.predicted_demand 
    for forecast in forecasts
    )

    target = sum(
    target.target_value
    for target in targets
    )
    
    if forecast > target:  #type:ignore
        recommendation = (
        "Demand expected to exceed targets. "
        "Consider increasing inventory capacity."
        )

    elif forecast < target: #type:ignore
        recommendation = (
        "Forecast below target. "
        "Consider promotional activities."
        )

    else:
        recommendation = (
        "Forecast aligned with targets."
        )
        
    return success_response(
        message="Planning recommendations generated",
        data={
        "recommendation": recommendation
        }
    )    