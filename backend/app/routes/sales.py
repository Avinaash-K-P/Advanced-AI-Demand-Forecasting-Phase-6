from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
import pandas as pd
from app.utils.response import success_response
from app.utils.logger import log_api_activity
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.sales import Sales
from app.services.forecast_service import auto_generate_forecast
from app.core.security import get_current_user, verify_role
from app.services.sales_service import (
    validate_dataset, 
    clean_dataset
)
from app.services.dataset_service import (
    create_dataset_version,
    log_upload_history
)
from app.models.user import User

router = APIRouter(prefix="/sales", tags=["Sales"])

# Upload Sales Dataset
@router.post("/upload-dataset")
async def upload_dataset(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db), 
    user = Depends(verify_role("analyst")),
    current_user: User = Depends(get_current_user)
):

    filename = file.filename.lower() #type: ignore

    try:

        # Read file
        file_contents = await file.read()
        file_size_kb = round(len(file_contents) / 1024, 2)

        # Re-read for pandas
        import io
        if filename.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(file_contents))
            file_type = "csv"
 
        elif filename.endswith(".xlsx"):
            df = pd.read_excel(io.BytesIO(file_contents))
            file_type = "xlsx"

        else:
            raise HTTPException(
                status_code=400,
                detail="Only CSV and Excel files are allowed"
            )
        
        # Validate dataset
        validation_error = validate_dataset(df)

        if validation_error:

            raise HTTPException(
                status_code=400,
                detail=validation_error
            )
        
        # Clean dataset
        df, cleaning_report = clean_dataset(df)

        sales_records = []

        # Create dataset version

        version = create_dataset_version(
            db=db,
            dataset_name=file.filename,
            file_type=file_type,
            total_rows=cleaning_report["cleaned_rows"],
            total_columns=len(df.columns),
            columns_list=list(df.columns),
            file_size_kb=file_size_kb,
            uploaded_by=current_user.id
        )

        for _, row in df.iterrows():

            sales = Sales(
                organization_id = current_user.organization_id,
                product_name=row["product_name"],
                category=row["category"],
                sales_date=row["sales_date"],
                quantity_sold=int(row["quantity_sold"]),
                revenue=float(row["revenue"]),
                region = row["region"],
                customer_id = row["customer_id"],
                product_id = row["product_id"],
                transaction_id = row["transaction_id"],
                customer_age = row["customer_age"],
                customer_gender = row["customer_gender"],
                customer_segment = row["customer_segment"] 
                )
            sales_records.append(sales)

        db.add_all(sales_records)
        db.commit() 

        # Adds to log uploads
        log_upload_history(
            db=db,
            dataset_version_id=version.id,
            dataset_name=file.filename,
            uploaded_by=current_user.id,
            upload_status="success",
            rows_uploaded=cleaning_report["original_rows"],
            rows_cleaned=cleaning_report["cleaned_rows"],
            duplicates_removed=cleaning_report["duplicates_removed"],
            cleaning_report=cleaning_report
        )


        print("Forecast will be generated in few seconds....")
        
        org_id  = current_user.organization_id
        
        auto_generate_forecast(org_id)  # Automatically generate the forecast results

        log_api_activity(

            db=db,

            user_id= user["id"],

            username= user["username"],

            endpoint="/upload-dataset",

            method="GET",

            status="SUCCESS"
        )    

        return success_response(
            message = "File uploaded successfully",
            data = {
                "columns": list(df.columns),
                "rows_after_cleaning": len(df),
                "cleaning_report": cleaning_report,
                "dataset_version": version.version_number
            }
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
