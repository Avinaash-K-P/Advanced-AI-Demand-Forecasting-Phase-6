from pydantic import BaseModel

class DataQualityReportCreate(BaseModel):

    organization_id: int
    dataset_id: int
    generated_by: str

class ValidationLogCreate(BaseModel):

    quality_report_id: int
    dataset_id: int
    validation_type: str
    severity: str
    message: str
    affected_records: str    