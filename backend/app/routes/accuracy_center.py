from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
import math
from datetime import datetime

from app.db.database import get_db
from app.models.user import User
from app.models.sales import Sales
from app.models.forecast_results import ForecastResult
from app.models.forecast_accuracy import ForecastAccuracy
from app.models.forecast_history import ForecastHistory
from app.models.model_metadata import ModelMetadata
from app.core.security import get_current_user,verify_role
from app.utils.response import success_response

router = APIRouter(prefix="/accuracy", tags=["Forecast Accuracy Center"])


# ──────────────────────────────────────────
# Helper — compute metrics from paired lists
# ──────────────────────────────────────────

def compute_metrics(actual: list, predicted: list) -> dict:
    """Compute MAE, RMSE, MAPE from actual vs predicted lists."""

    n = len(actual)
    if n == 0:
        return {"mae": None, "rmse": None, "mape": None}

    mae = sum(abs(a - p) for a, p in zip(actual, predicted)) / n

    rmse = math.sqrt(
        sum((a - p) ** 2 for a, p in zip(actual, predicted)) / n
    )

    mape_values = [
        abs((a - p) / a) * 100
        for a, p in zip(actual, predicted) if a != 0
    ]
    mape = sum(mape_values) / len(mape_values) if mape_values else None

    return {
        "mae": round(mae, 2),
        "rmse": round(rmse, 2),
        "mape": round(mape, 2) if mape else None
    }


def performance_label(mae: float) -> str:
    if mae is None:
        return "Unknown"
    if mae < 5:
        return "Excellent"
    elif mae < 15:
        return "Good"
    elif mae < 30:
        return "Fair"
    else:
        return "Needs Improvement"


# ──────────────────────────────────────────
# 7.1 — Model Performance Dashboard
# ──────────────────────────────────────────

@router.get("/model-performance")
def model_performance_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Full model performance summary dashboard.
    Returns MAE, RMSE, MAPE, per-model breakdown,
    average accuracy %, and overall performance label.
    """

    accuracy_rows = db.query(ForecastAccuracy).all()

    if not accuracy_rows:
        return success_response(
            message="No accuracy data available yet",
            data={}
        )

    # Overall metrics
    actual = [r.actual_demand for r in accuracy_rows]
    predicted = [r.predicted_demand for r in accuracy_rows]
    metrics = compute_metrics(actual, predicted)

    avg_accuracy = round(
        sum(r.accuracy_percentage for r in accuracy_rows) / len(accuracy_rows), 2
    )

    # Per model breakdown
    model_groups = {}
    for r in accuracy_rows:
        model = r.model_type or "Ensemble"
        if model not in model_groups:
            model_groups[model] = {"actual": [], "predicted": [], "accuracy": []}
        model_groups[model]["actual"].append(r.actual_demand)
        model_groups[model]["predicted"].append(r.predicted_demand)
        model_groups[model]["accuracy"].append(r.accuracy_percentage)

    per_model = []
    for model, values in model_groups.items():
        m = compute_metrics(values["actual"], values["predicted"])
        per_model.append({
            "model": model,
            "records_evaluated": len(values["actual"]),
            "avg_accuracy_pct": round(
                sum(values["accuracy"]) / len(values["accuracy"]), 2
            ),
            "mae": m["mae"],
            "rmse": m["rmse"],
            "mape": m["mape"],
            "performance": performance_label(m["mae"])
        })

    # Model metadata
    metadata = db.query(ModelMetadata).first()

    return success_response(
        message="Model performance dashboard fetched successfully!",
        data={
            "overall": {
                "total_records_evaluated": len(accuracy_rows),
                "avg_accuracy_pct": avg_accuracy,
                "mae": metrics["mae"],
                "rmse": metrics["rmse"],
                "mape": metrics["mape"],
                "performance_label": performance_label(metrics["mae"])
            },
            "per_model_breakdown": per_model,
            "model_metadata": {
                "last_trained_at": metadata.last_trained_at if metadata else None,
                "last_sales_count": metadata.last_sales_count if metadata else None
            }
        }
    )


# ──────────────────────────────────────────
# 7.2 — Forecast Accuracy Trends
# ──────────────────────────────────────────

@router.get("/accuracy-trends")
def accuracy_trends(
    period: Optional[str] = Query("monthly", description="daily / monthly"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns accuracy % trend over time grouped by day or month.
    Used to plot accuracy trend charts on the frontend.
    """

    accuracy_rows = db.query(ForecastAccuracy).order_by(
        ForecastAccuracy.evaluation_date.asc()
    ).all()

    if not accuracy_rows:
        return success_response(
            message="No accuracy trend data available",
            data=[]
        )

    grouped = {}

    for r in accuracy_rows:

        if period == "monthly":
            key = r.evaluation_date.strftime("%Y-%m")
        else:
            key = str(r.evaluation_date)

        if key not in grouped:
            grouped[key] = {"accuracy": [], "mae_values": [], "actual": [], "predicted": []}

        grouped[key]["accuracy"].append(r.accuracy_percentage)
        grouped[key]["actual"].append(r.actual_demand)
        grouped[key]["predicted"].append(r.predicted_demand)

    trend_data = []
    for period_key, values in grouped.items():
        m = compute_metrics(values["actual"], values["predicted"])
        trend_data.append({
            "period": period_key,
            "avg_accuracy_pct": round(
                sum(values["accuracy"]) / len(values["accuracy"]), 2
            ),
            "mae": m["mae"],
            "rmse": m["rmse"],
            "records": len(values["accuracy"])
        })

    return success_response(
        message="Accuracy trends fetched successfully!",
        data=trend_data
    )


# ──────────────────────────────────────────
# 7.3 — Compare Historical Prediction Performance
# ──────────────────────────────────────────

@router.get("/model-comparison")
def model_comparison(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Side-by-side comparison of Prophet, Linear Regression,
    and Moving Average predictions vs actual demand.
    """

    forecast_rows = db.query(ForecastResult).all()
    sales_rows = db.query(Sales).all()

    if not forecast_rows or not sales_rows:
        return success_response(
            message="Insufficient data for model comparison",
            data={}
        )

    # Build actual demand lookup by date
    actual_lookup = {}
    for s in sales_rows:
        key = str(s.sales_date)
        actual_lookup[key] = actual_lookup.get(key, 0) + s.quantity_sold

    prophet_actual, prophet_pred = [], []
    lr_actual, lr_pred = [], []
    ma_actual, ma_pred = [], []
    ensemble_actual, ensemble_pred = [], []

    for f in forecast_rows:
        key = str(f.forecast_date)
        actual = actual_lookup.get(key)
        if actual is None:
            continue

        if f.prophet_prediction is not None:
            prophet_actual.append(actual)
            prophet_pred.append(f.prophet_prediction)

        if f.lr_prediction is not None:
            lr_actual.append(actual)
            lr_pred.append(f.lr_prediction)

        if f.ma_prediction is not None:
            ma_actual.append(actual)
            ma_pred.append(f.ma_prediction)

        ensemble_actual.append(actual)
        ensemble_pred.append(f.predicted_demand)

    return success_response(
        message="Model comparison completed successfully!",
        data={
            "Prophet": {
                **compute_metrics(prophet_actual, prophet_pred),
                "records": len(prophet_actual),
                "performance": performance_label(
                    compute_metrics(prophet_actual, prophet_pred)["mae"]
                )
            },
            "Linear_Regression": {
                **compute_metrics(lr_actual, lr_pred),
                "records": len(lr_actual),
                "performance": performance_label(
                    compute_metrics(lr_actual, lr_pred)["mae"]
                )
            },
            "Moving_Average": {
                **compute_metrics(ma_actual, ma_pred),
                "records": len(ma_actual),
                "performance": performance_label(
                    compute_metrics(ma_actual, ma_pred)["mae"]
                )
            },
            "Ensemble": {
                **compute_metrics(ensemble_actual, ensemble_pred),
                "records": len(ensemble_actual),
                "performance": performance_label(
                    compute_metrics(ensemble_actual, ensemble_pred)["mae"]
                )
            }
        }
    )


# ──────────────────────────────────────────
# 7.4 — Track Model Improvement Over Time
# ──────────────────────────────────────────

@router.get("/model-improvement")
def model_improvement(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Tracks how model accuracy has improved across
    forecast runs by comparing monthly accuracy averages
    and computing improvement deltas between periods.
    """

    accuracy_rows = db.query(ForecastAccuracy).order_by(
        ForecastAccuracy.evaluation_date.asc()
    ).all()

    if len(accuracy_rows) < 2:
        return success_response(
            message="Not enough data to track improvement",
            data=[]
        )

    # Group by month
    monthly = {}
    for r in accuracy_rows:
        key = r.evaluation_date.strftime("%Y-%m")
        if key not in monthly:
            monthly[key] = []
        monthly[key].append(r.accuracy_percentage)

    periods = sorted(monthly.keys())
    improvement_data = []

    for i, period in enumerate(periods):
        avg_acc = round(sum(monthly[period]) / len(monthly[period]), 2)
        delta = None
        direction = None

        if i > 0:
            prev_avg = round(
                sum(monthly[periods[i - 1]]) / len(monthly[periods[i - 1]]), 2
            )
            delta = round(avg_acc - prev_avg, 2)
            direction = "improved" if delta > 0 else "declined" if delta < 0 else "stable"

        improvement_data.append({
            "period": period,
            "avg_accuracy_pct": avg_acc,
            "records": len(monthly[period]),
            "delta_from_previous": delta,
            "direction": direction
        })

    # Overall improvement summary
    first_acc = improvement_data[0]["avg_accuracy_pct"]
    last_acc = improvement_data[-1]["avg_accuracy_pct"]
    total_improvement = round(last_acc - first_acc, 2)

    return success_response(
        message="Model improvement tracking fetched successfully!",
        data={
            "improvement_timeline": improvement_data,
            "summary": {
                "first_period": periods[0],
                "latest_period": periods[-1],
                "first_accuracy_pct": first_acc,
                "latest_accuracy_pct": last_acc,
                "total_improvement_pct": total_improvement,
                "overall_direction": (
                    "improved" if total_improvement > 0
                    else "declined" if total_improvement < 0
                    else "stable"
                )
            }
        }
    )


# ──────────────────────────────────────────
# 7.5 — Generate Model Evaluation Report
# ──────────────────────────────────────────

@router.get("/evaluation-report")
def evaluation_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Generates a structured model evaluation report combining
    performance metrics, accuracy trends, model comparison,
    and improvement summary into one unified response.
    Ready to be consumed by PDF/Excel export on the frontend.
    """

    accuracy_rows = db.query(ForecastAccuracy).all()
    metadata = db.query(ModelMetadata).first()
    forecast_rows = db.query(ForecastResult).all()
    sales_rows = db.query(Sales).all()

    if not accuracy_rows:
        return success_response(
            message="No evaluation data available to generate report",
            data={}
        )

    # Overall metrics
    actual = [r.actual_demand for r in accuracy_rows]
    predicted = [r.predicted_demand for r in accuracy_rows]
    metrics = compute_metrics(actual, predicted)
    avg_accuracy = round(
        sum(r.accuracy_percentage for r in accuracy_rows) / len(accuracy_rows), 2
    )

    # Accuracy trend — monthly
    monthly = {}
    for r in accuracy_rows:
        key = r.evaluation_date.strftime("%Y-%m")
        if key not in monthly:
            monthly[key] = []
        monthly[key].append(r.accuracy_percentage)

    trend = [
        {
            "period": k,
            "avg_accuracy_pct": round(sum(v) / len(v), 2),
            "records": len(v)
        }
        for k, v in sorted(monthly.items())
    ]

    # Model comparison
    actual_lookup = {}
    for s in sales_rows:
        key = str(s.sales_date)
        actual_lookup[key] = actual_lookup.get(key, 0) + s.quantity_sold

    prophet_pairs = [
        (actual_lookup[str(f.forecast_date)], f.prophet_prediction)
        for f in forecast_rows
        if str(f.forecast_date) in actual_lookup and f.prophet_prediction
    ]
    lr_pairs = [
        (actual_lookup[str(f.forecast_date)], f.lr_prediction)
        for f in forecast_rows
        if str(f.forecast_date) in actual_lookup and f.lr_prediction
    ]
    ma_pairs = [
        (actual_lookup[str(f.forecast_date)], f.ma_prediction)
        for f in forecast_rows
        if str(f.forecast_date) in actual_lookup and f.ma_prediction
    ]

    model_comparison = {
        "Prophet": compute_metrics(
            [p[0] for p in prophet_pairs], [p[1] for p in prophet_pairs]
        ),
        "Linear_Regression": compute_metrics(
            [p[0] for p in lr_pairs], [p[1] for p in lr_pairs]
        ),
        "Moving_Average": compute_metrics(
            [p[0] for p in ma_pairs], [p[1] for p in ma_pairs]
        )
    }

    # Best model
    best_model = min(
        model_comparison,
        key=lambda m: model_comparison[m]["mae"] or float("inf")
    )

    return success_response(
        message="Model evaluation report generated successfully!",
        data={
            "report_generated_at": datetime.utcnow(),
            "generated_by": current_user.username,
            "overall_performance": {
                "total_records": len(accuracy_rows),
                "avg_accuracy_pct": avg_accuracy,
                "mae": metrics["mae"],
                "rmse": metrics["rmse"],
                "mape": metrics["mape"],
                "performance_label": performance_label(metrics["mae"])
            },
            "model_metadata": {
                "last_trained_at": metadata.last_trained_at if metadata else None,
                "total_sales_used": metadata.last_sales_count if metadata else None
            },
            "accuracy_trend": trend,
            "model_comparison": model_comparison,
            "best_performing_model": best_model,
            "recommendations": _generate_recommendations(
                metrics, avg_accuracy, model_comparison
            )
        }
    )


def _generate_recommendations(metrics, avg_accuracy, model_comparison) -> list:
    recs = []

    if avg_accuracy < 70:
        recs.append({
            "priority": "High",
            "message": "Overall accuracy is below 70%. Consider uploading more historical data."
        })
    elif avg_accuracy >= 90:
        recs.append({
            "priority": "Low",
            "message": "Model accuracy is excellent. Current forecasting setup is reliable."
        })

    if metrics["mape"] and metrics["mape"] > 20:
        recs.append({
            "priority": "Medium",
            "message": f"MAPE is {metrics['mape']}% — high percentage error. Review outliers in sales data."
        })

    best = min(model_comparison, key=lambda m: model_comparison[m]["mae"] or float("inf"))
    recs.append({
        "priority": "Low",
        "message": f"{best.replace('_', ' ')} is currently the best performing model with lowest MAE."
    })

    return recs