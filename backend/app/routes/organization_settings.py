from fastapi import APIRouter, Depends

from app.schemas.organization_settings import(
    OrganizationSettingsCreate,
    OrganizationSettingsUpdate
)

from app.services.organization_settings_service import (
    create_organization_settings,
    get_organization_settings_by_id,
    update_organization_settings
    
)

from app.core.security import verify_role

router = APIRouter(
    prefix="/organizations-settings",
    tags=["Organizations Settings"]
)

@router.post("/")
def add_organization_settings(
    Data: OrganizationSettingsCreate,
    user = Depends(verify_role("admins"))
):
    return create_organization_settings(Data)

@router.get("/{organization_settings_id}")
def fetch_organization_settings(
    org_settings_id: int,
    user = Depends(verify_role("admins"))
):
    return get_organization_settings_by_id(org_settings_id)

@router.put("/{organization_settings_id}")
def edit_organization_settings(
    org_settings_id: int,
    new_settings: OrganizationSettingsUpdate,
    user = Depends(verify_role("admins"))    
):
    return update_organization_settings(org_settings_id,new_settings)   