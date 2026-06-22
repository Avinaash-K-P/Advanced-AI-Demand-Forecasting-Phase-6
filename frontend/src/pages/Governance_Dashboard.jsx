import Layout from "../components/Layout";
import { useEffect, useState } from "react";
import api from "../services/api";
import { toast } from "react-toastify";

function Governance_Dashboard() {

  const darkMode = localStorage.getItem("theme") === "dark";    
  
  const [dashboardData, setDashboardData] =
  useState({
    total_revisions: 0,
    total_activities: 0,
    total_audit_logs: 0,
    approved_forecasts: 0,
    pending_forecasts: 0,
    rejected_forecasts: 0,
  });

  const [loading, setLoading] =
  useState(false);

  const fetchDashboard = async () => {

  try {

    setLoading(true);

    const response = await api.get(
      "/governance/dashboard"
    );

    setDashboardData(
      response.data.data
    );

  } catch (error) {

    console.error(error);

    toast.error(
      "Failed to load dashboard"
    );

  } finally {

    setLoading(false);

  }

};

const dashboardCards = [

  {
    title: "Total Revisions",
    value:
      dashboardData.total_revisions,
    icon: "📑",
  },

  {
    title: "Activities",
    value:
      dashboardData.total_activities,
    icon: "📈",
  },

  {
    title: "Audit Logs",
    value:
      dashboardData.total_audit_logs,
    icon: "📋",
  },

  {
    title: "Approved",
    value:
      dashboardData.approved_forecasts,
    icon: "✅",
  },

  {
    title: "Pending",
    value:
      dashboardData.pending_forecasts,
    icon: "⏳",
  },

  {
    title: "Rejected",
    value:
      dashboardData.rejected_forecasts,
    icon: "❌",
  },

];

useEffect(() => {
  fetchDashboard();
}, []);

    return(
    <Layout>

<div className="mb-8">

  <h1 className="text-3xl font-bold">
    Governance Dashboard
  </h1>

  <p
    className={`mt-2 ${
      darkMode
        ? "text-gray-400"
        : "text-gray-500"
    }`}
  >
    Monitor forecast governance,
    approvals, audit activities,
    and compliance metrics.
  </p>

</div>        
        
{
  loading && (
    <div className="mb-6">
      Loading governance dashboard...
    </div>
  )
  
}
        <div
  className="
    grid
    md:grid-cols-2
    lg:grid-cols-3
    gap-6
  "
>

  {dashboardCards.map(
    (card, index) => (

      <div
        key={index}
        className={`
          p-6
          rounded-2xl
          border
          shadow-lg

          ${
            darkMode
              ? "bg-gray-900 border-gray-800"
              : "bg-white border-gray-200"
          }
        `}
      >

        <div className="text-3xl mb-3">
          {card.icon}
        </div>

        <h3
          className="
            text-lg
            font-semibold
          "
        >
          {card.title}
        </h3>

        <p
          className="
            text-3xl
            font-bold
            mt-2
          "
        >
          {card.value}
        </p>

      </div>

    )
  )}

</div>

    </Layout>
    )

}

export default Governance_Dashboard;