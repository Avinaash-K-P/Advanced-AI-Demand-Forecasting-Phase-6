import Layout from "../components/Layout";
import { useState } from "react";
import api from "../services/api";
import { toast } from "react-toastify";

function Quarterly_Dashboard() {

  const darkMode =
    localStorage.getItem("theme") === "dark";

const [orgId, setOrgId] = useState("");

const [dashboardData, setDashboardData] = useState({
  quarterly_plans: null,
  business_targets: null,
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
      `/planning/quarterly-dashboard/${orgId}`
    );

    setDashboardData(
      response.data.data
    );

  } catch (error) {

    console.error(error);

    toast.error(
      "Failed to load quarterly dashboard"
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
            Quarterly Dashboard
          </h1>

          <p
            className={`mt-2 ${
              darkMode
                ? "text-gray-400"
                : "text-gray-500"
            }`}
          >
            Monitor quarterly plans and business targets.
          </p>

        </div>

        {/* Organization Input */}

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
        </div>

        {loading && (

  <div className="mb-6">
    Loading quarterly dashboard...
  </div>

)}

        {/* Quarterly Plan Card */}

        <div
  className={`
    rounded-2xl p-6 border shadow-lg mb-6
    ${
      darkMode
        ? "bg-gray-900 border-gray-800"
        : "bg-white border-gray-200"
    }
  `}
>

  <h2 className="text-xl font-semibold mb-4">
    Quarterly Plan
  </h2>

  {dashboardData.quarterly_plans ? (

    <div className="grid md:grid-cols-2 gap-4">

      <div>
        <p className="font-semibold">
          Name
        </p>
        <p>
          {dashboardData.quarterly_plans.name}
        </p>
      </div>

      <div>
        <p className="font-semibold">
          Quarter
        </p>
        <p>
          {dashboardData.quarterly_plans.quarter}
        </p>
      </div>

      <div>
        <p className="font-semibold">
          Year
        </p>
        <p>
          {dashboardData.quarterly_plans.year}
        </p>
      </div>

      <div>
        <p className="font-semibold">
          Status
        </p>
        <p>
          {dashboardData.quarterly_plans.status}
        </p>
      </div>

    </div>

  ) : (

    <p>No Quarterly Plan Found</p>

  )}

</div>

        {/* Business Target Card */}

     <div
  className={`
    rounded-2xl p-6 border shadow-lg
    ${
      darkMode
        ? "bg-gray-900 border-gray-800"
        : "bg-white border-gray-200"
    }
  `}
>

  <h2 className="text-xl font-semibold mb-4">
    Business Target
  </h2>

  {dashboardData.business_targets ? (

    <div className="grid md:grid-cols-2 gap-4">

      <div>
        <p className="font-semibold">
          Target Name
        </p>
        <p>
          {dashboardData.business_targets.target_name}
        </p>
      </div>

      <div>
        <p className="font-semibold">
          Target Type
        </p>
        <p>
          {dashboardData.business_targets.target_type}
        </p>
      </div>

      <div>
        <p className="font-semibold">
          Target Value
        </p>
        <p>
          {dashboardData.business_targets.target_value}
        </p>
      </div>

      <div>
        <p className="font-semibold">
          Status
        </p>
        <p>
          {dashboardData.business_targets.status}
        </p>
      </div>

    </div>

  ) : (

    <p>No Business Target Found</p>

  )}

</div>

      </div>

    </Layout>
  );
}

export default Quarterly_Dashboard;