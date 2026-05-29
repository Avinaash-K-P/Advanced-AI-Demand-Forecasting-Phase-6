Title: Advanced AI Demand Forecasting Phase 3

Backend: Python, Fast-api

Frontend: React.js

Database: MySQL Workbench

Analytics: Excel and Power BI

Dataset: Retail Sales Data (source:Kaggle.com)

IDE: Visual Studio Code

Backend packages:

Fast-api,
Uvicorn,
SQLAlchemy,
PyMySQL,
python-jose,
Passlib,
Pandas,
Scikit-learn,
OpenPyXL,
python-multipart,
ReportLab
Apscheduler
alembic
fastapi-cache2

Frontend packages:

React,
Vite,
Tailwind CSS,
Axios,
React Router DOM,
Recharts,
React Toastify,
exceljs,
file-saver,
jspdf,
jspdf-autotable

Database Tables:

1. Users - To store admin and users
2. Sales - To store the dataset
3. Forecast_results - To store the generated forecast prediction
4. Reports - To store the forecast report files created by users
5. Forecast_history - To store forecast history
6. Api_logs - To store the user activity

Features Added:

1. Dataset
  - Added a real time dataset  
  - Used Retail Sales Data from kaggle.com
  - Used Excel and Power BI tool to filter the dataset 
  - Total number of rows 12,140 

2. Dashboard
   - Global search feature
   - Search result table
   - Live dashboard activity
   - Automatic forecast refresh 
   - Real-time product monitoring
   - Automatic forecast generation model 
   - System performance metrics
   - Anomaly detection
   - Seasonal Trends
   - Region-wise forecast insight
   - Category-wise sales insight
   - Revenue prediction insight
   - Inventory risk analysis
   - Forecast history comparison 

3. Roles and Access Management
   - Super Admin (can access everything)
   - Analyst (can upload sales, generate forecast and download reports)
   - Viewer (Only able to view dashboard and download reports) 
   - API's restriction to corresponding roles 

4. Frontend
   - Dark and Light theme
   - Interactive dynamic dashboard
   - Advanced filter method
   - Pagination features for sales data and forecast 
   - Special sidebar navigations
   - Interactive Charts and graphs

5. Optimization
   - Optimized sales data which consist more than 12,000 rows  
   - Added Caching support for dashboard API  
   - Added indexing and established relationship in database
   - Optimized forecast data by pagination

6. Reusable Components
   - Reusable common layout of sidebars 
   - Reusable dynamic dashboard
   - Dark and light mode theme in sidebars
   - Common notification icon
   - Common API pages for all designated roles  