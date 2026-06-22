from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.models.forecast_results import ForecastResult
from app.models.reports import Report
from app.models.forecast_accuracy import ForecastAccuracy
from app.core.security import verify_role, get_current_user
from app.utils.response import success_response
from app.utils.logger import log_api_activity
import pandas as pd
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from datetime import datetime
import os

router = APIRouter(prefix="/reports", tags=["Reports"])

REPORTS_DIR = "reports/forecast_reports"


# ── List All Reports ──
@router.get("/")
def list_reports(
    db: Session = Depends(get_db),
    user=Depends(verify_role("all"))
):
    reports = db.query(Report).order_by(Report.created_at.desc()).all()
    return success_response(
        message="Reports fetched successfully!",
        data=[{
            "id": r.id,
            "filename": r.filename,
            "file_type": r.file_type,
            "generated_by": r.generated_by,
            "created_at": r.created_at
        } for r in reports]
    )


# ── Export Enriched Excel ──
@router.get("/export-excel")
def export_excel(
    db: Session = Depends(get_db),
    user=Depends(verify_role("all")),
    current_user: User = Depends(get_current_user)
):
    forecasts = db.query(ForecastResult).order_by(
        ForecastResult.forecast_date.asc()
    ).all()

    accuracy_lookup = {
        str(r.evaluation_date): r.accuracy_percentage
        for r in db.query(ForecastAccuracy).all()
    }

    data = [{
        "Forecast Date":        row.forecast_date,
        "Predicted Demand":     round(row.predicted_demand, 2),
        "Prophet Prediction":   round(row.prophet_prediction, 2) if row.prophet_prediction else "N/A",
        "LR Prediction":        round(row.lr_prediction, 2) if row.lr_prediction else "N/A",
        "MA Prediction":        round(row.ma_prediction, 2) if row.ma_prediction else "N/A",
        "Confidence Score (%)": round(row.confidence_score, 2),
        "Sales Trend":          round(row.sales_trend, 2),
        "Accuracy (%)":         accuracy_lookup.get(str(row.forecast_date), "N/A")
    } for row in forecasts]

    df = pd.DataFrame(data)
    filename = f"forecast_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    file_path = os.path.join(REPORTS_DIR, filename)

    with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Forecast Report")
        ws = writer.sheets["Forecast Report"]
        for col in ws.columns:
            ws.column_dimensions[col[0].column_letter].width = 22

    report = Report(
        organization_id = current_user.organization_id,
        filename=filename,
        file_path=file_path,
        file_type="excel",
        generated_by=current_user.username
    )
    db.add(report)
    db.commit()

    log_api_activity(
        db=db,
        user_id= current_user.id,
        username=user["username"],
        endpoint="/export-excel",
        method="GET",
        status="SUCCESS"
    )

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


# ── Export Enriched PDF ──
@router.get("/export-pdf")
def export_pdf(
    db: Session = Depends(get_db),
    user=Depends(verify_role("all")),
    current_user: User = Depends(get_current_user)
):
    forecasts = db.query(ForecastResult).order_by(
        ForecastResult.forecast_date.asc()
    ).all()

    accuracy_lookup = {
        str(r.evaluation_date): r.accuracy_percentage
        for r in db.query(ForecastAccuracy).all()
    }

    filename  = f"forecast_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    file_path = os.path.join(REPORTS_DIR, filename)

    doc      = SimpleDocTemplate(file_path, pagesize=A4)
    styles   = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("AI Demand Forecast Report", styles["Title"]))
    elements.append(Paragraph(
        f"Generated: {datetime.now().strftime('%B %d, %Y %H:%M')} | By: {current_user.username}",
        styles["Normal"]
    ))
    elements.append(Spacer(1, 20))

    table_data = [
        ["Date", "Predicted", "Confidence", "Trend", "Accuracy"]
    ] + [
        [
            str(f.forecast_date),
            round(f.predicted_demand, 2),
            f"{round(f.confidence_score, 1)}%",
            round(f.sales_trend, 2),
            f"{accuracy_lookup.get(str(f.forecast_date), 'N/A')}%"
        ]
        for f in forecasts
    ]

    table = Table(table_data, colWidths=[110, 100, 90, 80, 80])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#065f46")),
        ("TEXTCOLOR",  (0, 0), (-1, 0), colors.white),
        ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0fdf4")]),
        ("GRID",   (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("PADDING", (0, 0), (-1, -1), 6)
    ]))

    elements.append(table)
    doc.build(elements)

    report = Report(
        organization_id = current_user.organization_id,
        filename=filename,
        file_path=file_path,
        file_type="pdf",
        generated_by=current_user.username
    )
    db.add(report)
    db.commit()

    log_api_activity(
        db=db,
        user_id= current_user.id,
        username=user["username"],
        endpoint="/export-pdf",
        method="GET",
        status="SUCCESS"
    )

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/pdf"
    )