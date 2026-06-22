from app.db.session import SessionLocal
from app.models.data_quality_reports import DataQualityReports
from app.models.dataset_validation_logs import DatasetValidationLogs
from app.models.sales import Sales
from app.utils.response import success_response, error_response

def generate_data_quality_report(
    organization_id: int,
    dataset_id: int,
    generated_by: str
):

    db = SessionLocal()

    try:

        sales = (
            db.query(Sales)
            .filter(
                Sales.organization_id == organization_id
            )
            .all()
        )

        total_records = len(sales)

        valid_records = 0
        missing_count = 0

        for row in sales:

            if row.sales_date and row.quantity_sold:

                valid_records += 1

            else:

                missing_count += 1

        invalid_records = total_records - valid_records

        score = (
            (valid_records / total_records) * 100
            if total_records > 0 else 0
        )

        report = DataQualityReports(

            organization_id=organization_id,
            dataset_id=dataset_id,

            overall_score=round(score, 2),

            total_records=total_records,
            valid_records=valid_records,
            invalid_records=invalid_records,

            duplicate_records=0,
            missing_value_count=missing_count,
            outlier_count=0,

            status="Completed",

            generated_by=generated_by
        )

        db.add(report)
        db.commit()

        return success_response(
            message="Data quality report generated",
            data={
                "quality_score": score
            }
        )

    except Exception as e:

        db.rollback()

        return error_response(
            message="Report generation failed",
            details=str(e)
        )

    finally:

        db.close()


def create_validation_log(payload):

    db = SessionLocal()

    try:

        log = DatasetValidationLogs(

            quality_report_id=payload.quality_report_id,
            dataset_id=payload.dataset_id,

            validation_type=payload.validation_type,
            severity=payload.severity,

            message=payload.message,
            affected_records=payload.affected_records
        )

        db.add(log)
        db.commit()

        return success_response(
            message="Validation log created"
        )

    except Exception as e:

        db.rollback()

        return error_response(
            message="Failed to create validation log",
            details=str(e)
        )

    finally:

        db.close()

def detect_incomplete_dataset(
    organization_id: int
):

    db = SessionLocal()

    try:

        sales = (
            db.query(Sales)
            .filter(
                Sales.organization_id == organization_id
            )
            .all()
        )

        issues = []

        for row in sales:

            if not row.sales_date:

                issues.append(
                    "Missing sales_date"
                )

            if not row.quantity_sold:

                issues.append(
                    "Missing quantity_sold"
                )

        return success_response(
            message="Dataset validation completed",
            data={
                "issue_count": len(issues),
                "issues": issues
            }
        )

    finally:

        db.close()

def get_quality_report(
    report_id: int
):

    db = SessionLocal()

    try:

        report = (
            db.query(DataQualityReports)
            .filter(
                DataQualityReports.id == report_id
            )
            .first()
        )

        return success_response(
            message="Quality report retrieved",
            data=report
        )

    finally:

        db.close()

def get_validation_summary(
    report_id: int
):

    db = SessionLocal()

    try:

        logs = (
            db.query(DatasetValidationLogs)
            .filter(
                DatasetValidationLogs.quality_report_id
                == report_id
            )
            .all()
        )

        return success_response(
            message="Validation summary retrieved",
            data=logs
        )

    finally:

        db.close()

def get_quality_dashboard_metrics(
    organization_id: int
):

    db = SessionLocal()

    try:

        reports = (
            db.query(DataQualityReports)
            .filter(
                DataQualityReports.organization_id
                == organization_id
            )
            .all()
        )

        if not reports:

            return success_response(
                message="No reports found",
                data={}
            )

        latest = reports[-1]

        return success_response(
            message="Dashboard metrics retrieved",
            data={
                "quality_score":
                    latest.overall_score,

                "valid_records":
                    latest.valid_records,

                "invalid_records":
                    latest.invalid_records,

                "duplicates":
                    latest.duplicate_records,

                "missing_values":
                    latest.missing_value_count,

                "outliers":
                    latest.outlier_count
            }
        )

    finally:

        db.close()                                        