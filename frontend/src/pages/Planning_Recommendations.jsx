import Layout from "../components/Layout";
import { useState } from "react";
import api from "../services/api";
import { toast } from "react-toastify";

function Planning_Recommendations() {

  const darkMode =
    localStorage.getItem("theme") === "dark";

  const [orgId, setOrgId] = useState("");

  const [recommendation, setRecommendation] =
  useState("");

  const [loading, setLoading] =
  useState(false);

  const fetchRecommendation = async () => {

  if (!orgId) {

    toast.error(
      "Please enter Organization ID"
    );

    return;

  }

  try {

    setLoading(true);

    const response = await api.get(
      `/planning/recommendations/${orgId}`
    );

    setRecommendation(
      response.data.data.recommendation
    );

  } catch (error) {

    console.error(error);

    toast.error(
      "Failed to load recommendation"
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
            Planning Recommendations
          </h1>

          <p
            className={`mt-2 ${
              darkMode
                ? "text-gray-400"
                : "text-gray-500"
            }`}
          >
            AI-generated strategic planning insights
            based on forecast and target analysis.
          </p>

        </div>

        {/* Organization Input */}

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
            onClick={fetchRecommendation}
            className="
              mt-4
              px-6 py-3
              rounded-xl
              bg-blue-600
              text-white
              hover:bg-blue-700
            "
          >
            Generate Recommendation
          </button>

          {
  loading && (
    <div className="mb-6">
      Generating recommendation...
    </div>
  )
}
                      
        </div>

        {/* Recommendation Card */}

        <div
          className={`
            rounded-2xl border shadow-lg p-8
            ${
              darkMode
                ? "bg-gray-900 border-gray-800"
                : "bg-white border-gray-200"
            }
          `}
        >

          <div className="flex items-center gap-3 mb-6">

            <div className="text-4xl">
              🤖
            </div>

            <div>

              <h2 className="text-2xl font-semibold">
                AI Recommendation
              </h2>

              <p
                className={
                  darkMode
                    ? "text-gray-400"
                    : "text-gray-500"
                }
              >
                Strategic Planning Assistant
              </p>

            </div>

          </div>

          <div
            className={`
              rounded-xl p-6
              ${
                darkMode
                  ? "bg-gray-800"
                  : "bg-gray-50"
              }
            `}
          >

            <p
            className={`
              text-lg leading-relaxed
              font-medium
              ${
                darkMode
                  ? "text-green-300"
                  : "text-green-700"
              }
            `}
          >
            {
              recommendation
                ? recommendation
                : "Recommendation will appear here after loading organization data."
            }
          </p>
          
          </div>

        </div>

      </div>

    </Layout>
  );
}

export default Planning_Recommendations;