import Layout from "../components/Layout";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import { toast } from "react-toastify";

function View_Workflows() {

  const navigate = useNavigate();

  const darkMode =
    localStorage.getItem("theme") === "dark";

  const [workflows, setWorkflows] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const fetchWorkflows = async () => {

    try {

      const response = await api.get(
        "/workflow/"
      );

      setWorkflows(
        response.data.data || []
      );

    } catch (error) {

      console.error(error);

      toast.error(
        "Failed to load workflows"
      );

    } finally {

      setLoading(false);

    }
  };

  useEffect(() => {

    fetchWorkflows();

  }, []);

  return (
    <Layout>

      <div className="p-8">

        {/* Header */}
        <div className="mb-8">

          <h1 className="text-3xl font-bold">
            Workflow Library
          </h1>

          <p
            className={`mt-2 ${
              darkMode
                ? "text-gray-400"
                : "text-gray-500"
            }`}
          >
            View and manage workflow automation
            processes.
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
            Loading workflows...
          </div>

        )}

        {/* Empty State */}
        {!loading &&
          workflows.length === 0 && (

          <div
            className={`
              rounded-2xl
              p-8
              text-center
              border
              ${
                darkMode
                  ? "bg-gray-900 border-gray-800"
                  : "bg-white border-gray-200"
              }
            `}
          >
            No workflows found.
          </div>

        )}

        {/* Workflow Cards */}
        {!loading &&
          workflows.length > 0 && (

          <div
            className="
              grid
              grid-cols-1
              md:grid-cols-2
              lg:grid-cols-3
              gap-6
            "
          >

            {workflows.map((workflow) => (

              <div
                key={workflow.id}
                className={`
                  rounded-2xl
                  border
                  p-6
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

                <div className="flex justify-between items-start mb-4">

                  <h2 className="text-xl font-semibold">
                    {workflow.name}
                  </h2>

                  <span
                    className={`
                      px-3 py-1 rounded-full text-xs
                      ${
                        workflow.is_active
                          ? "bg-green-100 text-green-700"
                          : "bg-red-100 text-red-700"
                      }
                    `}
                  >
                    {workflow.is_active
                      ? "Active"
                      : "Inactive"}
                  </span>

                </div>

                <p
                  className={`mb-4 text-sm ${
                    darkMode
                      ? "text-gray-400"
                      : "text-gray-500"
                  }`}
                >
                  {workflow.description ||
                    "No description available"}
                </p>

                <div className="space-y-2 text-sm">

                  <p>
                    <strong>Type:</strong>{" "}
                    {workflow.workflow_type}
                  </p>

                  <p>
                    <strong>Trigger:</strong>{" "}
                    {workflow.trigger_event}
                  </p>

                  <p>
                    <strong>Organization:</strong>{" "}
                    {workflow.organization_id}
                  </p>

                  <p>
                    <strong>Created By:</strong>{" "}
                    {workflow.created_by}
                  </p>

                </div>

                <div className="mt-6">

                  <button
                    onClick={() =>
                      navigate(
                        "/workflow/step/create"
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
                    Add Steps
                  </button>

                </div>

              </div>

            ))}

          </div>

        )}

      </div>

    </Layout>
  );
}

export default View_Workflows;