from fastapi import APIRouter, Depends

from app.schemas.organization import (
    OrganizationCreate,
    OrganizationUpdate
)

from app.services.organization_service import (
    create_organization,
    get_organizations,
    get_organization_by_id,
    update_organization,
    delete_organization
)

from app.core.security import verify_role

router = APIRouter(
    prefix="/organizations",
    tags=["Organizations"]
)


@router.post("/")
def add_organization(
    organization: OrganizationCreate,
    user = Depends(verify_role("admin"))
):
    return create_organization(organization)


@router.get("/")
def list_organizations(
    user = Depends(verify_role("admin"))
):
    return get_organizations()


@router.get("/{organization_id}")
def fetch_organization(
    organization_id: int,
    user = Depends(verify_role("admin"))
):
    return get_organization_by_id(
        organization_id
    )


@router.put("/{organization_id}")
def edit_organization(
    organization_id: int,
    organization: OrganizationUpdate,
    user = Depends(verify_role("admin"))
):
    return update_organization(
        organization_id,
        organization
    )


@router.delete("/{organization_id}")
def remove_organization(
    organization_id: int,
    user = Depends(verify_role("admin"))
):
    return delete_organization(
        organization_id
    )



