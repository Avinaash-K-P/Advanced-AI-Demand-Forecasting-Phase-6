import Layout from "../components/Layout";
import { useState } from "react";
import api from "../services/api";
import { toast } from "react-toastify";

function Forecast_Vs_Target() {

  const darkMode =
    localStorage.getItem("theme") === "dark";

const [orgId, setOrgId] = useState("");

const [comparisonData, setComparisonData] = useState({
  target: 0,
  forecast: 0,
  variance: 0,
});

const [loading, setLoading] = useState(false);

const fetchComparison = async () => {

  if (!orgId) {

    toast.error(
      "Please enter Organization ID"
    );

    return;
  }

  try {

    setLoading(true);

    const response = await api.get(
      `/planning/forecast-vs-target/${orgId}`
    );

    setComparisonData(
      response.data.data
    );

  } catch (error) {

    console.error(error);

    toast.error(
      "Failed to load comparison data"
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
            Forecast vs Target
          </h1>

          <p
            className={`mt-2 ${
              darkMode
                ? "text-gray-400"
                : "text-gray-500"
            }`}
          >
            Compare forecasted demand against business targets.
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
  onClick={fetchComparison}
  className="
    mt-4
    px-6 py-3
    rounded-xl
    bg-blue-600
    text-white
    hover:bg-blue-700
  "
>
  Compare Forecast vs Target
</button>

{
  loading && (
    <div className="mb-6">
      Loading comparison...
    </div>
  )
}

        </div>

        {/* KPI Cards */}

        <div className="grid md:grid-cols-3 gap-6 mb-8">

          <div
            className={`
              rounded-2xl p-6 shadow-lg border
              ${
                darkMode
                  ? "bg-gray-900 border-gray-800"
                  : "bg-white border-gray-200"
              }
            `}
          >

            <h3 className="font-semibold text-lg">
              Business Target
            </h3>

            <p className="text-3xl font-bold mt-3">
              {comparisonData.target}
            </p>

          </div>

          <div
            className={`
              rounded-2xl p-6 shadow-lg border
              ${
                darkMode
                  ? "bg-gray-900 border-gray-800"
                  : "bg-white border-gray-200"
              }
            `}
          >

            <h3 className="font-semibold text-lg">
              Forecast Demand
            </h3>

            <p className="text-3xl font-bold mt-3">
              {comparisonData.forecast}
            </p>

          </div>

          <div
            className={`
              rounded-2xl p-6 shadow-lg border
              ${
                darkMode
                  ? "bg-gray-900 border-gray-800"
                  : "bg-white border-gray-200"
              }
            `}
          >

            <h3 className="font-semibold text-lg">
              Variance
            </h3>

            <p className="text-3xl font-bold mt-3">
              {comparisonData.variance}
            </p>

          </div>

        </div>

        {/* Summary */}

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
            Analysis Summary
          </h2>

          <p
            className={
              darkMode
                ? "text-gray-300"
                : "text-gray-700"
            }
          >
          
            {comparisonData.variance > 0
              ? `Forecast exceeds target by ${comparisonData.variance}. Consider increasing inventory, production capacity, and workforce planning.`
              : comparisonData.variance < 0
              ? `Forecast is below target by ${Math.abs(
                  comparisonData.variance
                )}. Consider promotions, marketing campaigns, or sales initiatives.`
              : "Forecast is perfectly aligned with business targets."
            }

          </p>
          
        </div>

      </div>

    </Layout>
  );
}

export default Forecast_Vs_Target;