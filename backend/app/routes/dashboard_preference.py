from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.security import get_current_user, verify_role
from app.db.database import get_db
from app.models.dashboard_preference import DashboardPreference
from app.schemas.dashboard_preference import DashboardPreferenceUpdate
from app.utils.response import success_response


router = APIRouter(prefix="/dashboard", tags=["Dasboard Preference"])

@router.get("/preferences")
def get_preferences(

    db: Session = Depends(get_db),

    current_user = Depends(get_current_user),

    user = Depends(verify_role("all"))

):

    pref = db.query(
        DashboardPreference
    ).filter(

        DashboardPreference.user_id
        ==
        current_user.id

    ).first()

    if not pref:

        pref = DashboardPreference(
            user_id=current_user.id
        )

        db.add(pref)

        db.commit()

        db.refresh(pref)

    return success_response(
        message = "Dashboard Preference Fetched",
        data=pref.__dict__
    )

@router.put("/preferences")
def save_preferences(

    request: DashboardPreferenceUpdate,

    db: Session = Depends(get_db),

    current_user = Depends(get_current_user),

    user = Depends(verify_role("all"))

):

    pref = db.query(
        DashboardPreference
    ).filter(

        DashboardPreference.user_id
        ==
        current_user.id

    ).first()

    if not pref:

        pref = DashboardPreference(
            user_id=current_user.id
        )

        db.add(pref)

    pref.show_kpi = request.show_kpi

    pref.show_revenue = request.show_revenue

    pref.show_profit = request.show_profit

    pref.show_growth = request.show_growth

    pref.show_cost = request.show_cost

    pref.show_ai_insights = request.show_ai_insights

    db.commit()

    return success_response(
        message="Preferences saved"
    )