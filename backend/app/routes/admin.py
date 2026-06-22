from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.database import get_db
from app.utils.response import success_response
from app.utils.pagination import paginator
from app.core.security import get_current_user, verify_role
from app.models.forecast_results import ForecastResult
from app.models.user import User
from app.models.sales import Sales
from app.models.reports import Report
import os
from datetime import datetime
from app.schemas.auth import UserStatusUpdate
from app.models.api_logs import APILog
from app.schemas.auth import UserRoleOrganizationUpdate

router = APIRouter(prefix="/admin", tags=["Admin"])

# Dashboard 
@router.get("/dashboard")
def admin_dashboard(
    db: Session = Depends(get_db), 
    admin = Depends(verify_role("admins"))
):
    total_users = db.query(User).count()
    total_datasets = db.query(Sales).count()
    total_forecasts = db.query(ForecastResult).count()
    total_revenue = db.query(func.sum(Sales.revenue)).scalar() 
    return success_response(
        message="Welcome to the Admin Dashboard!",
        data={
            "total_users": total_users,
            "total_datasets": total_datasets,
            "total_forecasts": total_forecasts,
            "total_revenue": total_revenue or 0.0
        }
        )

# List All Users 
@router.get("/users")
def list_users(
    id: int = None,
    username:str=None,
    role:str=None,
    db: Session = Depends(get_db), 
    admin = Depends(verify_role("admins"))
):
    query = db.query(User)
    
    if id:
        query = query.filter(User.id == id)
    
    if username:
        query = query.filter(User.username.ilike(f"%{username}%"))

    if role: 
        query = query.filter(User.role == role)

    data = query.all()
    return success_response(
        message="List of all users",
        data= data
    )

# User Management
@router.put("/users/{user_id}/status")
def update_user_status(

    user_id: int,

    payload: UserStatusUpdate,

    db: Session = Depends(get_db),

    admin = Depends(verify_role("admins"))

):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        raise HTTPException(

            status_code=404,

            detail="User not found"

        )

    user.status = payload.status

    db.commit()

    return {

        "message":
        "Status updated successfully"
    }

# Role and Organization management
@router.put("/users/{user_id}/role")
def update_user_role(

    user_id: int,

    payload: UserRoleOrganizationUpdate,

    db: Session = Depends(get_db),

    admin = Depends(
        verify_role(
            ["super_admin", "organization_admin"]
        )
    )

):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if (admin.role == "organization_admin"
        and
        user.organization_id != admin.organization_id):

        raise HTTPException(
            status_code=403,
            detail="Cannot manage users from another organization"
        )

    user.role = payload.role

    user.organization_id = payload.organization_id

    db.commit()

    db.refresh(user)

    return success_response(
        message="User role updated successfully",
        data={
            "user_id": user.id,
            "role": user.role,
            "organization_id": user.organization_id
        }
    )



# Activity Logs
@router.get("/activity-logs")
def get_activity_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "super_admin":

        raise HTTPException(

        status_code=403,

        detail="Access denied"
    )
    logs = (

    db.query(APILog)

    .order_by(
        APILog.timestamp.desc()
    )

    .all()
)
    
    return success_response(

        message="Activity logs fetched",

        data=[

        {

            "user_id":
            log.user_id,

            "username":
            log.username,

            "endpoint":
            log.endpoint,

            "method":
            log.method,

            "status":
            log.status,

            "timestamp":
            log.timestamp

        }

        for log in logs

    ]
)

# List All Sales 
@router.get("/sales")
def list_sales(
    skip: int = 0,
    limit: int = 10,
    product_name:str = None,
    category:str = None,
    start_date: str = None,
    end_date: str = None,
    region:str = None,
    db: Session = Depends(get_db), 
    admin = Depends(verify_role("admins"))
):
    query = db.query(Sales) 

    if product_name:
        query = query.filter(Sales.product_name.ilike(f"%{product_name}%"))

    if category:
        query = query.filter(Sales.category == category)
        
    if start_date:
        query = query.filter(Sales.sales_date >= start_date)

    if end_date:
        query = query.filter(Sales.sales_date <= end_date)

    if region:
        query = query.filter(Sales.region == region)

    data = paginator(query,skip,limit) 
    return success_response(
        message="List of all sales data",
        data= data
    )

# View Reports 
@router.get("/reports")
def view_reports(
    db: Session = Depends(get_db), 
    admin = Depends(verify_role("admins"))
):
    reports_folder = "reports"
    
    data = []

    if os.path.exists(reports_folder):

        files = os.listdir(reports_folder)

        for file in files:

            file_path = os.path.join(reports_folder,file)

            data.append({

                "file_name": file,

                "file_path": file_path,

                "file_type": file.split(".")[-1],

                "created_at": datetime.fromtimestamp(
                    os.path.getctime(file_path)
                )
            })

    return success_response(
        message="List of all generated reports",
        data=data
    )        


# List All Forecasts 
@router.get("/forecasts")
def list_forecasts(
    skip: int = 0,
    limit: int = 10,
    start_date: str = None,
    end_date: str = None,
    db: Session = Depends(get_db), 
    admin = Depends(verify_role("admins"))
):
    query = db.query(ForecastResult)
    
    if start_date:
        query = query.filter(ForecastResult.forecast_date >= start_date)

    if end_date:
        query = query.filter(ForecastResult.forecast_date <= end_date)

    data = paginator(query,skip,limit)
    return success_response(
        message="List of all forecast results",
        data=data
    )
