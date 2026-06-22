import Layout from "../components/Layout";
import { useEffect, useState } from "react";
import api from "../services/api";
import { toast } from "react-toastify";

function Workflow_Executions() {

  const darkMode =
    localStorage.getItem("theme") === "dark";

  const [executions, setExecutions] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const fetchExecutions = async () => {

    try {

      const response = await api.get(
        "/workflow/executions"
      );

      setExecutions(
        response.data.data || []
      );

    } catch (error) {

      console.error(error);

      toast.error(
        "Failed to load workflow executions"
      );

    } finally {

      setLoading(false);

    }
  };

  useEffect(() => {

    fetchExecutions();

  }, []);

  return (
    <Layout>

      <div className="p-8">

        {/* Header */}
        <div className="mb-8">

          <h1 className="text-3xl font-bold">
            Workflow Executions
          </h1>

          <p
            className={`mt-2 ${
              darkMode
                ? "text-gray-400"
                : "text-gray-500"
            }`}
          >
            Monitor workflow execution history and status.
          </p>

        </div>

        {/* Loading */}
        {loading && (
          <div
            className={`text-center py-8 ${
              darkMode
                ? "text-gray-400"
                : "text-gray-500"
            }`}
          >
            Loading executions...
          </div>
        )}

        {/* Empty State */}
        {!loading &&
          executions.length === 0 && (

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
            No workflow executions found.
          </div>

        )}

        {/* Execution Table */}
        {!loading &&
          executions.length > 0 && (

          <div
            className={`
              rounded-2xl
              border
              overflow-hidden
              shadow-lg
              ${
                darkMode
                  ? "bg-gray-900 border-gray-800"
                  : "bg-white border-gray-200"
              }
            `}
          >

            <div className="overflow-x-auto">

              <table className="w-full">

                <thead
                  className={
                    darkMode
                      ? "bg-gray-800"
                      : "bg-gray-100"
                  }
                >
                  <tr>

                    <th className="p-4 text-left">
                      ID
                    </th>

                    <th className="p-4 text-left">
                      Workflow
                    </th>

                    <th className="p-4 text-left">
                      Organization
                    </th>

                    <th className="p-4 text-left">
                      Status
                    </th>

                    <th className="p-4 text-left">
                      Triggered By
                    </th>

                    <th className="p-4 text-left">
                      Started
                    </th>

                    <th className="p-4 text-left">
                      Completed
                    </th>

                  </tr>
                </thead>

                <tbody>

                  {executions.map(
                    (execution) => (

                    <tr
                      key={execution.id}
                      className={`
                        border-t
                        ${
                          darkMode
                            ? "border-gray-800"
                            : "border-gray-200"
                        }
                      `}
                    >

                      <td className="p-4">
                        {execution.id}
                      </td>

                      <td className="p-4">
                        {execution.workflow_id}
                      </td>

                      <td className="p-4">
                        {execution.organization_id}
                      </td>

                      <td className="p-4">

                        <span
                          className={`
                            px-3 py-1 rounded-full text-xs font-medium
                            ${
                              execution.status ===
                              "Completed"
                                ? "bg-green-100 text-green-700"
                                : "bg-yellow-100 text-yellow-700"
                            }
                          `}
                        >
                          {execution.status}
                        </span>

                      </td>

                      <td className="p-4">
                        {execution.triggered_by}
                      </td>

                      <td className="p-4">
                        {execution.started_at}
                      </td>

                      <td className="p-4">
                        {execution.completed_at}
                      </td>

                    </tr>

                  ))}

                </tbody>

              </table>

            </div>

          </div>

        )}

      </div>

    </Layout>
  );
}

export default Workflow_Executions;