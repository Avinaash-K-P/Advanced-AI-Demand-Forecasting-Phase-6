import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Dashboard from './pages/User_Dashboard';
import Login from './pages/Login';
import Register from './pages/Register';
import Profile from './pages/Profile';
import UploadDataset from './pages/UploadDataset';
import Forecast from './pages/Forecast';
import Reports from './pages/Reports';
import AdminUsers from './pages/Admin_Users';
import AdminSales from './pages/Admin_Sales';
import AdminForecast from './pages/Admin_Forecast';
import AdminReports from './pages/Admin_Reports';
import DownloadSummary from './pages/Analytics_Summary';
import Unauthorized from './pages/Unauthorized';
import ProtectedRoute from './components/Protected_routes';
import IntegrationManagement from './pages/Integration_Management';
import ActivityLogs from './pages/Activity_Logs';
import ForgotPassword from './pages/forgot_password';
import ResetPassword from './pages/reset_password';
import Management from './pages/Admin_Management';
import Senario from './pages/Test_Scenario';
import ProjectDetail from './pages/Project_Detail';
import ProjectSettings from './pages/Project_Settings';
import Projects from './pages/Projects';
import Workspace from './pages/Workspace';
import ExecutiveDashboard from './pages/Executive_Dashboard';
import Collaboration from './pages/Collaboration';
import CollaborationInvitations from './pages/Collaboration_Invitations';
import ProjectDiscussion from './pages/Project_Discussion';
import ForecastComments from './pages/Forecast_comments';
import ReportSharing from './pages/Report_Sharing';
import DownloadReports from './pages/Download_Reports';
import DashboardSettings from './pages/Dashboard_Settings';
import Organization from "./pages/Organization";

// Phase 6 Modules
import Create_Organization from './pages/Create_Organization';
import View_Organizations from './pages/View_Organizations';
import Organization_Details from './pages/Organization_Details';
import Organization_Settings from './pages/Organization_Settings';
import Workflow from './pages/Workflow';
import Create_Workflow from './pages/Create_Workflow';
import View_Workflows from './pages/Workflow_List';
import Execute_Workflow from './pages/Workflow_Execute';
import Workflow_Executions from './pages/Workflow_Executions';
import Create_Workflow_Step from './pages/Workflow_Steps';
import Workflow_Logs from './pages/Workflow_Logs';
import Strategic_Planning from './pages/Strategic_Planning';
import Create_Annual_Plan from './pages/Create_Annual_Plan';
import Create_Quarterly_Plan from './pages/Create_Quarterly_Plan';
import Create_Business_Target from './pages/Create_Business_Target';
import Annual_Dashboard from './pages/Annual_Dashboard';
import Quarterly_Dashboard from './pages/Quarterly_Dashboard';
import Forecast_Vs_Target from './pages/Forecast_Vs_Target';
import Planning_Recommendations from './pages/Planning_Recommendations';
import Governance from './pages/Governance';
import Governance_Dashboard from './pages/Governance_Dashboard';
import Forecast_Versions from './pages/Forecast_Versions';
import Activity_Timeline from './pages/Activity_Timeline';
import Audit_Logs from './pages/Audit_Logs';
import Forecast_Lifecycle from './pages/Forecast_Lifecycle';


function App() {


  return (

     <BrowserRouter>

      <Routes>

        <Route
          path="/"
          element={<Login />}
        />

        <Route
          path="/register"
          element={<Register />}
        />

        <Route
          path="/forgot-password"
          element={<ForgotPassword/>}
        />

        <Route
          path="/reset-password"
          element={<ResetPassword/>}
        />

        <Route
          path="/profile"
          element={ <Profile />}
        />  

        <Route
          path="/dashboard"
          element={<Dashboard />}
        />

        <Route
          path="/upload"
          element={<UploadDataset />}
        />

        <Route
          path="/forecast"
          element={<Forecast/>}
        />

        <Route
          path="/download"
          element={<DownloadReports />}
        />

        <Route
          path="/download/forecast-report"
          element={<Reports />}
        />

        <Route
        path="/download/analytic-summary"
        element={ <DownloadSummary />}
        />

        <Route
          path="/executive-dashboard"
          element={ <ExecutiveDashboard />}
        />

          <Route
          path="/admin/management"
          element={<Management />}
        />

        <Route
          path="/admin/management/users"
          element={ <AdminUsers />}
        />


        <Route
          path="/admin/management/sales"
          element={<AdminSales />}
        />

          <Route
          path="/admin/management/forecasts"
          element={<AdminForecast />}
        />
          <Route
          path="/admin/management/reports"
          element={<AdminReports />}
        />

        <Route
          path="/admin/management/integration"
          element={<IntegrationManagement />}
        />

        <Route
          path="/admin/activity-logs"
          element={ <ActivityLogs />}
        />    
        
        <Route
          path = "/forecast-scenario"
          element = { <Senario />} 
        />

        <Route
          path = "/workspace"
          element = { <Workspace /> } 
        />  

        <Route
          path = "/workspace/projects"
          element = { <Projects />} 
        />  

          <Route
          path = "/workspace/project-details"
          element = {<ProjectDetail />} 
        />  

          <Route
          path = "/workspace/project-settings"
          element = {<ProjectSettings />} 
        />    

          <Route
          path = "/workspace/project-discussions"
          element = {<ProjectDiscussion />} 
        />    

          <Route
        path="/collaboration"
        element={ <Collaboration />}
        />

          <Route
        path="/collaboration/invitation"
        element={<CollaborationInvitations />}
        />

          <Route
        path="/collaboration/project-discussion"
        element={<ProjectDiscussion />}
      />

          <Route
        path="/collaboration/forecast-comments"
        element={<ForecastComments />}
      />  

        <Route
        path="/collaboration/report-sharing"
        element={<ReportSharing />}
      />

        <Route
        path="/dashboard/settings"
        element={<DashboardSettings/>}
      />

        <Route
          path="/organization"
          element={<Organization />}
        />

        <Route
          path="/organization/create"
          element={<Create_Organization />}
        />

        <Route
          path="/organization/view"
          element={<View_Organizations />}
        />

        <Route
          path="/organization/details/:id"
          element={<Organization_Details />}
        />

        <Route
          path="/organization/settings"
          element={<Organization_Settings />}
        />

        <Route
          path="/workflow"
          element={<Workflow />}
        />

        <Route
          path="/workflow/create"
          element={<Create_Workflow/>}
        />

        <Route
          path="/workflow/view"
          element={<View_Workflows />}
        />

        <Route
          path="/workflow/execute"
          element={<Execute_Workflow />}
        />

        <Route
          path="/workflow/executions"
          element={<Workflow_Executions />}
        />

        <Route
          path="/workflow/steps"
          element={<Create_Workflow_Step />}
        />

        <Route
          path="/workflow/logs"
          element={<Workflow_Logs />}
        />

        <Route
          path="/planning"
          element={<Strategic_Planning />}
        />

        <Route
          path="/planning/annual"
          element={<Create_Annual_Plan />}
        />

        <Route
          path="/planning/quarterly"
          element={<Create_Quarterly_Plan />}
        />

        <Route
          path="/planning/targets"
          element={<Create_Business_Target />}
        />
        <Route
          path="/planning/annual-dashboard"
         element={<Annual_Dashboard />}
        />

        <Route
          path="/planning/quarterly-dashboard"
          element={<Quarterly_Dashboard />}
        />

        <Route
          path="/planning/forecast-vs-target"
          element={<Forecast_Vs_Target />}
        />

        <Route
          path="/planning/recommendations"
          element={<Planning_Recommendations />}
        />

        <Route
          path="/governance"
          element={<Governance />}
        />

        <Route
          path="/governance/versions"
          element={<Forecast_Versions />}
        />

        <Route
          path="/governance/activity-timeline"
          element={<Activity_Timeline />}
        />

        <Route
          path="/governance/audit-logs"
          element={<Audit_Logs />}
        />

        <Route
          path="/governance/lifecycle"
          element={<Forecast_Lifecycle />}
        />

        <Route
          path="/governance/dashboard"
          element={<Governance_Dashboard />}
        />

        <Route 
        path="/unauthorized"
        element={<Unauthorized/>}
        />

      </Routes>

    </BrowserRouter>

  );

}

export default App;