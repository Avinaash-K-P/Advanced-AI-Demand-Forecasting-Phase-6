import Layout from "../components/Layout";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import { toast } from "react-toastify";

function View_Organizations() {

  const navigate = useNavigate();

  const darkMode =
    localStorage.getItem("theme") === "dark";

  const [organizations, setOrganizations] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const fetchOrganizations = async () => {

    try {

      const response = await api.get(
        "/organizations/"
      );

      setOrganizations(
        response.data.data || []
      );

    } catch (error) {

      console.error(error);

      toast.error(
        "Failed to load organizations"
      );

    } finally {

      setLoading(false);

    }
  };

  useEffect(() => {

    fetchOrganizations();

  }, []);

  return (
    <Layout>

      <div className="p-8">

        {/* Header */}
        <div className="mb-8">

          <h1 className="text-3xl font-bold">
            Organizations
          </h1>

          <p
            className={`mt-2 ${
              darkMode
                ? "text-gray-400"
                : "text-gray-500"
            }`}
          >
            View and manage all organizations.
          </p>

        </div>

        {/* Loading */}
        {loading && (

          <div
            className={`text-center py-10 ${
              darkMode
                ? "text-gray-400"
                : "text-gray-500"
            }`}
          >
            Loading organizations...
          </div>

        )}

        {/* Empty State */}
        {!loading &&
          organizations.length === 0 && (

          <div
            className={`
              rounded-2xl p-8 text-center border
              ${
                darkMode
                  ? "bg-gray-900 border-gray-800"
                  : "bg-white border-gray-200"
              }
            `}
          >
            No organizations found.
          </div>

        )}

        {/* Organization Cards */}
        {!loading &&
          organizations.length > 0 && (

          <div
            className="
              grid
              grid-cols-1
              md:grid-cols-2
              lg:grid-cols-3
              gap-6
            "
          >

            {organizations.map((org) => (

              <div
                key={org.id}
                className={`
                  rounded-2xl
                  p-6
                  border
                  shadow-lg
                  transition
                  hover:shadow-xl
                  ${
                    darkMode
                      ? "bg-gray-900 border-gray-800"
                      : "bg-white border-gray-200"
                  }
                `}
              >

                <h2 className="text-xl font-semibold mb-2">
                  {org.name}
                </h2>

                <p
                  className={`mb-2 ${
                    darkMode
                      ? "text-gray-400"
                      : "text-gray-500"
                  }`}
                >
                  Code: {org.code}
                </p>

                <p
                  className={`mb-4 ${
                    darkMode
                      ? "text-gray-400"
                      : "text-gray-500"
                  }`}
                >
                  {org.industry || "No Industry"}
                </p>

                <button
                  onClick={() =>
                    navigate(
                      `/organization/details/${org.id}`
                    )
                  }
                  className="
                    w-full
                    py-2
                    rounded-xl
                    bg-green-600
                    hover:bg-green-700
                    text-white
                  "
                >
                  View Details
                </button>

              </div>

            ))}

          </div>

        )}

      </div>

    </Layout>
  );
}

export default View_Organizations;