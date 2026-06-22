from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse 
from app.utils.response import error_response
from app.db.session import engine, Base 
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.utils.apscheduler import scheduler
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

# Routes Imports
from app.routes import(
    auth, 
    admin, 
    sales, 
    forecast, 
    analytics, 
    reports, 
    inventory_integration, 
    alert_settings, 
    forecast_projects, 
    scenario, 
    business_intelligence, 
    ai_insight, 
    forecast_comments, 
    report_sharing,
    collaboration, 
    forecast_timeline,
    forecast_revision, 
    data_managment,
    accuracy_center, 
    executive_reports,
    dashboard_preference,
    organization,
    organization_settings,
    approval_workflow,
    workflow,
    strategic_planning,
    governance,
    kpi,
    data_quality,
    executive_commands,
    notification
    )

# Models Imports

from app.models.user import User
from app.models.sales import Sales
from app.models.forecast_results import ForecastResult
from app.models.reports import Report
from app.models.model_metadata import ModelMetadata
from app.models.api_logs import APILog
from app.models.forecast_history import ForecastHistory
from app.models.forecast_scheduler import ForecastSchedule
from app.models.alerts import Alert
from app.models.Inventory_Integration import InventoryIntegration
from app.models.inventory import Inventory
from app.models.forecast_accuracy import ForecastAccuracy
from app.models.alert_settings import AlertSettings
from app.models.forecast_project import ForecastProject
from app.models.project_member import ProjectMember
from app.models.project_dataset import ProjectDataset
from app.models.project_forecast import ProjectForecast
from app.models.project_report import ProjectReport
from app.models.project_activity import ProjectActivity
from app.models.ai_insight import AIInsight
from app.models.forecast_comments import ForecastComment
from app.models.report_sharing import ReportShare
from app.models.project_collaboration import CollaborationInvitation
from app.models.project_discussion import ProjectDiscussion
from app.models.forecast_activity_timeline import ForecastActivityTimeline
from app.models.forecast_revision import ForecastRevision
from app.models.dataset_version import DatasetVersion
from app.models.dataset_upload_history import DatasetUploadHistory
from app.models.dataset_modification import DatasetModification
from app.models.report_schedule import ReportSchedule
from app.models.dashboard_preference import DashboardPreference

#--------------------PHASE 6 MODELS------------------------------------

from app.models.organization import Organization
from app.models.organization_settings import OrganizationSettings
from app.models.forecast_approval import ForecastApproval
from app.models.forecast_approval_history import ForecastApprovalHistory
from app.models.workflow import Workflow
from app.models.workflow_steps import Workflowsteps
from app.models.workflow_executions import WorkflowExecution
from app.models.workflow_logs import WorkflowLogs
from app.models.annual_plans import AnnualPlans
from app.models.quarterly_plans import QuarterlyPlans
from app.models.business_targets import BusinessTargets
from app.models.forecast_lifecycle import ForecastLifecycle
from app.models.governance_audit_logs import GovernanceAuditLogs
from app.models.kpis import Kpis
from app.models.kpi_values import KPIValues
from app.models.kpi_alerts import KPIAlerts
from app.models.data_quality_reports import DataQualityReports
from app.models.dataset_validation_logs import DatasetValidationLogs
from app.models.executive_dashboard import ExecutiveDashboard
from app.models.executive_alerts import ExecutiveAlerts
from app.models.notification import Notifications
from app.models.notification_preference import NotificationPreferences
from app.models.notification_history import NotificationHistory

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Demand Forecasting Platform",
    description="""
Enterprise-grade AI Demand Forecasting and Planning Platform.

Features:
- Multi-Organization Management
- New Role-Based Access Control
- Sales Data Management
- AI Forecast Generation
- Forecast Approval Workflows
- Workflow Automation
- Strategic Planning Dashboards
- Forecast Governance Center
- KPI Management
- Data Quality Monitoring
- Executive Command Center
- Notification Center
- Organization-Based Data Isolation
- Audit Logging and Compliance Tracking
""",
    version="6.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(admin.router)

# ---- Phase 6 routes--------------------------
app.include_router(organization.router)
app.include_router(organization_settings.router)
app.include_router(approval_workflow.router)
app.include_router(workflow.router)
app.include_router(strategic_planning.router)
app.include_router(governance.router)
app.include_router(kpi.router)
app.include_router(data_quality.router)
app.include_router(executive_commands.router)
app.include_router(notification.router)
#----------------------------------------------

app.include_router(sales.router)
app.include_router(forecast.router)
app.include_router(reports.router)
app.include_router(analytics.router)

app.include_router(accuracy_center.router)
app.include_router(dashboard_preference.router)
app.include_router(data_managment.router)
app.include_router(business_intelligence.router)
app.include_router(ai_insight.router)
app.include_router(forecast_projects.router)
app.include_router(forecast_comments.router)
app.include_router(collaboration.router)
app.include_router(report_sharing.router)
app.include_router(executive_reports.router)
app.include_router(forecast_timeline.router)
app.include_router(forecast_revision.router)
app.include_router(scenario.router)
app.include_router(inventory_integration.router)
app.include_router(alert_settings.router)


# Caching Support
@app.on_event("startup")
async def startup():

    FastAPICache.init(
        InMemoryBackend(),
        prefix="fastapi-cache"
    )


# To view the excel and pdf file
app.mount(
    "/reports",StaticFiles(directory="reports"),name="reports"
)

@app.get("/")
def home():
    return {"message": "API is running successfully!"}


# Global Exception Handling
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(exc.detail)
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    formatted_errors = []

    for err in exc.errors():
        formatted_errors.append({
            "field": err["loc"][-1],
            "message": err["msg"]
        })

    return JSONResponse(
        status_code=422,
        content=error_response(
            message=f"Validation failed: {formatted_errors}"
        )
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):

    print("UNEXPECTED ERROR:", exc)

    return JSONResponse(
        status_code=500,
        content=error_response("Internal Server Error")
    )