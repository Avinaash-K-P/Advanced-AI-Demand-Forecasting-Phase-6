import Layout from "../components/Layout";
import { useState } from "react";
import { toast } from "react-toastify";
import api from "../services/api";

function Annual_Dashboard() {

  const darkMode =
    localStorage.getItem("theme") === "dark";

const [orgId, setOrgId] = useState("");

const [dashboardData, setDashboardData] = useState({
  annual_plans: [],
  business_targets: [],
  forecast_count: 0,
});

const [loading, setLoading] = useState(false);

const fetchDashboard = async () => {

  if (!orgId) {

    toast.error(
      "Please enter Organization ID"
    );

    return;

  }

  try {

    setLoading(true);

    const response = await api.get(
      `/planning/annual-dashboard/${orgId}`
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

  return (
    <Layout>

      <div className="p-8">

        {/* Header */}

        <div className="mb-8">

          <h1 className="text-3xl font-bold">
            Annual Dashboard
          </h1>

          <p
            className={`mt-2 ${
              darkMode
                ? "text-gray-400"
                : "text-gray-500"
            }`}
          >
            View annual plans, targets and forecasting statistics.
          </p>

        </div>

        {/* Organization Selector */}

        <div
          className={`
            p-6 rounded-2xl border mb-8
            ${
              darkMode
                ? "bg-gray-900 border-gray-800"
                : "bg-white border-gray-200"
            }
          `}
        >

          <label className="block mb-2 font-medium">
            Organization ID
          </label>

          <input
            type="number"
            value={orgId}
            onChange={(e) =>
              setOrgId(e.target.value)
            }
            placeholder="Enter Organization ID"
            className={`
              w-full p-3 rounded-xl border
              ${
                darkMode
                  ? "bg-gray-800 border-gray-700"
                  : "bg-white border-gray-300"
              }
            `}
          />

          <button
  onClick={fetchDashboard}
  className="
    mt-4
    px-6
    py-3
    rounded-xl
    bg-blue-600
    text-white
    hover:bg-blue-700
  "
>
  Load Dashboard
</button>

        {loading && (

  <div className="mb-6">
    Loading dashboard...
  </div>

)}


        </div>

        {/* KPI Cards */}


        <div className="grid md:grid-cols-3 gap-6 mb-8">

          <div
            className={`
              p-6 rounded-2xl border shadow-lg
              ${
                darkMode
                  ? "bg-gray-900 border-gray-800"
                  : "bg-white border-gray-200"
              }
            `}
          >
            <h3 className="text-lg font-semibold">
              Annual Plans
            </h3>

            <p className="text-3xl font-bold mt-3">
              {dashboardData.annual_plans?.length || 0}
            </p>
          </div>

          <div
            className={`
              p-6 rounded-2xl border shadow-lg
              ${
                darkMode
                  ? "bg-gray-900 border-gray-800"
                  : "bg-white border-gray-200"
              }
            `}
          >
            <h3 className="text-lg font-semibold">
              Business Targets
            </h3>

            <p className="text-3xl font-bold mt-3">
              {dashboardData.business_targets?.length || 0}
            </p>
          </div>

          <div
            className={`
              p-6 rounded-2xl border shadow-lg
              ${
                darkMode
                  ? "bg-gray-900 border-gray-800"
                  : "bg-white border-gray-200"
              }
            `}
          >
            <h3 className="text-lg font-semibold">
              Forecast Count
            </h3>

            <p className="text-3xl font-bold mt-3">
              {dashboardData.forecast_count || 0}
            </p>
          </div>

        </div>

        {/* Annual Plans */}

        <div
          className={`
            rounded-2xl border p-6 mb-8
            ${
              darkMode
                ? "bg-gray-900 border-gray-800"
                : "bg-white border-gray-200"
            }
          `}
        >

          <h2 className="text-xl font-semibold mb-4">
            Annual Plans
          </h2>

          <div className="overflow-x-auto">

            <table className="w-full">

              <thead>

                <tr
                  className={
                    darkMode
                      ? "border-gray-700"
                      : "border-gray-200"
                  }
                >
                  <th className="text-left p-3">
                    Name
                  </th>

                  <th className="text-left p-3">
                    Year
                  </th>

                  <th className="text-left p-3">
                    Status
                  </th>
                </tr>

              </thead>

              <tbody>

{dashboardData.annual_plans?.length > 0 ? (

  dashboardData.annual_plans.map((plan) => (

    <tr
      key={plan.id}
      className="border-t"
    >
      <td className="p-3">
        {plan.name}
      </td>

      <td className="p-3">
        {plan.year}
      </td>

      <td className="p-3">
        {plan.status}
      </td>
    </tr>

  ))

) : (

  <tr>
    <td
      colSpan="3"
      className="p-4 text-center"
    >
      No Plans Found
    </td>
  </tr>

)}

              </tbody>

            </table>

          </div>

        </div>

        {/* Business Targets */}

        <div
          className={`
            rounded-2xl border p-6
            ${
              darkMode
                ? "bg-gray-900 border-gray-800"
                : "bg-white border-gray-200"
            }
          `}
        >

          <h2 className="text-xl font-semibold mb-4">
            Business Targets
          </h2>

          <div className="overflow-x-auto">

            <table className="w-full">

              <thead>

                <tr>
                  <th className="text-left p-3">
                    Target Name
                  </th>

                  <th className="text-left p-3">
                    Type
                  </th>

                  <th className="text-left p-3">
                    Value
                  </th>

                  <th className="text-left p-3">
                    Status
                  </th>
                </tr>

              </thead>

              <tbody>

{dashboardData.business_targets?.length > 0 ? (

  dashboardData.business_targets.map((target) => (

    <tr
      key={target.id}
      className="border-t"
    >
      <td className="p-3">
        {target.target_name}
      </td>

      <td className="p-3">
        {target.target_type}
      </td>

      <td className="p-3">
        {target.target_value}
      </td>

      <td className="p-3">
        {target.status}
      </td>
    </tr>

  ))

) : (

  <tr>
    <td
      colSpan="4"
      className="p-4 text-center"
    >
      No Targets Found
    </td>
  </tr>

)}

              </tbody>

            </table>

          </div>

        </div>

      </div>

    </Layout>
  );
}

export default Annual_Dashboard;