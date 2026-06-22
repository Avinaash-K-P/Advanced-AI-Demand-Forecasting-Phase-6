import Layout from "../components/Layout";
import api from "../services/api";
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";

function Governance() {

  const navigate = useNavigate();

  const darkMode = localStorage.getItem("theme") === "dark";

  const governanceModules = [

  {
    icon: "📊",
    title: "Governance Dashboard",
    description:
      "View governance KPIs and forecast approval metrics.",
    route: "/governance/dashboard",
  },

  {
    icon: "📝",
    title: "Forecast Versions",
    description:
      "Track forecast revision history and versions.",
    route: "/governance/versions",
  },

  {
    icon: "📅",
    title: "Activity Timeline",
    description:
      "Monitor forecast activities and lifecycle events.",
    route: "/governance/activity-timeline",
  },

  {
    icon: "📋",
    title: "Audit Logs",
    description:
      "Review governance audit records.",
    route: "/governance/audit-logs",
  },

  {
    icon: "🔄",
    title: "Forecast Lifecycle",
    description:
      "Manage forecast approval status and lifecycle stages.",
    route: "/governance/lifecycle",
  },

];

  return (

    <Layout>

      <div className="p-8">

        {/* Header */}

        <div className="mb-8">

          <h1 className="text-3xl font-bold">
            Governance Center
          </h1>

          <p
            className={`mt-2 ${
              darkMode
                ? "text-gray-400"
                : "text-gray-500"
            }`}
          >
            Monitor forecast governance, audit trails,
            lifecycle management, and compliance activities.
          </p>

        </div>

        {/* Governance Cards */}

        <div
          className="
            grid
            md:grid-cols-2
            lg:grid-cols-3
            gap-6
          "
        >

          {governanceModules.map(
            (module, index) => (

            <div
              key={index}
              className={`
                p-6
                rounded-2xl
                border
                shadow-lg
                cursor-pointer
                transition
                hover:scale-105
                ${
                  darkMode
                    ? "bg-gray-900 border-gray-800"
                    : "bg-white border-gray-200"
                }
              `}
              onClick={() => navigate(module.route)}
            >

              <div className="text-4xl mb-4">
                {module.icon}
              </div>
              
              <h2 className="text-xl font-semibold mb-3">
                {module.title}
              </h2>
              
              <p
                className={
                  darkMode
                    ? "text-gray-400"
                    : "text-gray-600"
                }
              >
                {module.description}
              </p>
              
            </div>

            )
          )}

        </div>

      </div>

    </Layout>

  );

}

export default Governance;