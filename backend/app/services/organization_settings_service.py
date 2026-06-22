from app.db.session import SessionLocal
from app.models.organization import Organization
from app.models.organization_settings import OrganizationSettings

from app.schemas.organization_settings import (
    OrganizationSettingsCreate,
    OrganizationSettingsUpdate
)

from app.utils.response import (
    success_response,
    error_response
)

def create_organization_settings(
    Data: OrganizationSettingsCreate
): 
    db = SessionLocal()
    try:
        
        existing_org = (
            db.query(OrganizationSettings)
            .filter(
                OrganizationSettings.organization_id == Data.organization_id
            )
            .first()
            
        )
        
        if existing_org:
            return error_response(
                message = "Organization settings already exists",
            )

        new_data = OrganizationSettings(
    
            organization_id = Data.organization_id,

            timezone = Data.timezone,     

            currency = Data.currency,

            forecast_retention_days = Data.forecast_retention_days,  

            default_forecast_model = Data.default_forecast_model,

            notifications_enabled = Data.notifications_enabled
        )     

        db.add(new_data)
        db.commit()
        db.refresh(new_data)

        return success_response(
            message="Organization Settings Created",
                   data={
                   "organization_settings_id": new_data.id
            }
        )
    
    except Exception as e:

        db.rollback()

        return error_response(
        message="Failed to create organization settings",
        details=str(e),
    )

    finally:

        db.close()

def get_organization_settings_by_id(
    org_settings_id: int
):

    db = SessionLocal()

    try:

        organization_settings = (
            db.query(OrganizationSettings)
            .filter(
                OrganizationSettings.id == org_settings_id
            )
            .first()
        )

        return success_response(
            message="Organization settings retrieved successfully",
            data = organization_settings
        )

    finally:

        db.close()

def update_organization_settings(
    settings_id: int,
    settings_data: OrganizationSettingsUpdate
):

    db = SessionLocal()

    try:

        organization_settings = (
            db.query(OrganizationSettings)
            .filter(
                OrganizationSettings.id == settings_id
            )
            .first()
        )

        if not organization_settings:

            return error_response(
                message = "Organization settings not found",
            )

        update_data = (
            settings_data.model_dump(
                exclude_unset=True
            )
        )

        for key, value in update_data.items():

            setattr(
                organization_settings,
                key,
                value
            )

        db.commit()

        return success_response (           
            message="Organization settings updated successfully"
            )

    except Exception as e:

        db.rollback()

        return error_response(
            message = "Organization settings not updated",
            details=str(e)
        )

    finally:

        db.close()
    