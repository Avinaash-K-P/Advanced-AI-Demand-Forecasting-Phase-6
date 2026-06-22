from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.utils.response import success_response, error_response

from app.models.organization import Organization
from app.schemas.organization import (
    OrganizationCreate,
    OrganizationUpdate
)

def create_organization(
    organization_data: OrganizationCreate,
):
    db = SessionLocal()

    try:

        existing_org = (
            db.query(Organization)
            .filter(
                Organization.code == organization_data.code
            )
            .first()
        )

        if existing_org:
            return error_response(
                message = "Organization code already exists"
            )


        organization = Organization(
            name=organization_data.name,
            code=organization_data.code,
            industry=organization_data.industry,
            description=organization_data.description,
            contact_email=organization_data.contact_email,
            contact_phone=organization_data.contact_phone,
            address=organization_data.address,
            country=organization_data.country
        )

        db.add(organization)
        db.commit()
        db.refresh(organization)

        return success_response(
        message="Organization created successfully",
        data={
        "organization_id": organization.id
        }
    )   

    except Exception as e:

        db.rollback()

        return error_response(
        message="Failed to create organization",
        details=str(e),
        code="ORGANIZATION_CREATE_ERROR"
    )

    finally:

        db.close()


def get_organizations():

    db = SessionLocal()

    try:

        organizations = db.query(
            Organization
        ).all()

        return success_response(
            message="Organizations retrieved successfully",
            data = organizations
        )

    finally:

        db.close()


def get_organization_by_id(
    organization_id: int
):

    db = SessionLocal()

    try:

        organization = (
            db.query(Organization)
            .filter(
                Organization.id == organization_id
            )
            .first()
        )

        return success_response(
            message="Organization retrieved successfully",
            data = organization
        )

    finally:

        db.close()

def update_organization(
    organization_id: int,
    organization_data: OrganizationUpdate
):

    db = SessionLocal()

    try:

        organization = (
            db.query(Organization)
            .filter(
                Organization.id == organization_id
            )
            .first()
        )

        if not organization:

            return error_response(
                message = "Organization not found",
            )

        update_data = (
            organization_data.model_dump(
                exclude_unset=True
            )
        )

        for key, value in update_data.items():

            setattr(
                organization,
                key,
                value
            )

        db.commit()

        return success_response (           
            message="Organization updated successfully"
            )

    except Exception as e:

        db.rollback()

        return error_response(
            message = "Organization not updated",
            details=str(e)
        )


    finally:

        db.close()


def delete_organization(
    organization_id: int
):

    db = SessionLocal()

    try:

        organization = (
            db.query(Organization)
            .filter(
                Organization.id == organization_id
            )
            .first()
        )

        if not organization:

            return error_response(
                message="Organization not found",
            )

        db.delete(organization)
        db.commit()

        return success_response(
            message = "Organization deleted successfully"
        ) 

    except Exception as e:

        db.rollback()

        return error_response(
            message="Organization not deleted",
            details = str(e)
        )

    finally:

        db.close()