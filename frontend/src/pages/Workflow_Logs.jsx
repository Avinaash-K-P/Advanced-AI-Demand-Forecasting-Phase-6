import Layout from "../components/Layout";
import { useEffect, useState } from "react";
import api from "../services/api";
import { toast } from "react-toastify";

function Workflow_Logs() {

  const darkMode =
    localStorage.getItem("theme") === "dark";

  const [logs, setLogs] = useState([]);

  const [loading, setLoading] =
    useState(true);

  const fetchLogs = async () => {

    try {

      const response = await api.get(
        "/workflow/logs"
      );

      setLogs(
        response.data.data || []
      );

    } catch (error) {

      console.error(error);

      toast.error(
        "Failed to load workflow logs"
      );

    } finally {

      setLoading(false);

    }
  };

  useEffect(() => {

    fetchLogs();

  }, []);

  return (
    <Layout>

      <div className="p-8">

        {/* Header */}
        <div className="mb-8">

          <h1 className="text-3xl font-bold">
            Workflow Logs
          </h1>

          <p
            className={`mt-2 ${
              darkMode
                ? "text-gray-400"
                : "text-gray-500"
            }`}
          >
            Monitor workflow events,
            execution messages, and audit logs.
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
            Loading workflow logs...
          </div>

        )}

        {/* Empty State */}
        {!loading &&
          logs.length === 0 && (

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
            No workflow logs found.
          </div>

        )}

        {/* Logs Table */}
        {!loading &&
          logs.length > 0 && (

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
                      Log ID
                    </th>

                    <th className="p-4 text-left">
                      Execution ID
                    </th>

                    <th className="p-4 text-left">
                      Step ID
                    </th>

                    <th className="p-4 text-left">
                      Level
                    </th>

                    <th className="p-4 text-left">
                      Message
                    </th>

                  </tr>
                </thead>

                <tbody>

                  {logs.map((log) => (

                    <tr
                      key={log.id}
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
                        {log.id}
                      </td>

                      <td className="p-4">
                        {log.workflow_execution_id}
                      </td>

                      <td className="p-4">
                        {log.workflow_step_id}
                      </td>

                      <td className="p-4">

                        <span
                          className={`
                            px-3 py-1 rounded-full text-xs font-medium
                            ${
                              log.log_level === "ERROR"
                                ? "bg-red-100 text-red-700"
                                : log.log_level === "WARNING"
                                ? "bg-yellow-100 text-yellow-700"
                                : "bg-green-100 text-green-700"
                            }
                          `}
                        >
                          {log.log_level}
                        </span>

                      </td>

                      <td className="p-4">
                        {log.message}
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

export default Workflow_Logs;