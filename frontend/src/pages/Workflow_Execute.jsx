import Layout from "../components/Layout";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import { toast } from "react-toastify";

function Execute_Workflow() {

  const navigate = useNavigate();

  const darkMode =
    localStorage.getItem("theme") === "dark";

  const [formData, setFormData] = useState({
    workflow_id: "",
    organization_id: "",
    triggered_by: "",
    execution_context: "",
  });

  const handleChange = (e) => {

    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });

  };

  const handleSubmit = async (e) => {

    e.preventDefault();

    try {

      const payload = {
        workflow_id: Number(
          formData.workflow_id
        ),
        organization_id: Number(
          formData.organization_id
        ),
        triggered_by: formData.triggered_by,
        execution_context:
          formData.execution_context,
      };

      const response = await api.post(
        "/workflow/execute",
        payload
      );

      console.log(response.data);

      toast.success(
        "Workflow executed successfully"
      );

      setFormData({
        workflow_id: "",
        organization_id: "",
        triggered_by: "",
        execution_context: "",
      });

      navigate(
        "/workflow/executions"
      );

    } catch (error) {

      console.error(error);

      toast.error(
        error?.response?.data?.message ||
        "Failed to execute workflow"
      );
    }
  };

  return (
    <Layout>

      <div className="p-8 max-w-4xl mx-auto">

        <div className="mb-8">

          <h1 className="text-3xl font-bold">
            Execute Workflow
          </h1>

          <p
            className={`mt-2 ${
              darkMode
                ? "text-gray-400"
                : "text-gray-500"
            }`}
          >
            Trigger and execute an
            existing workflow.
          </p>

        </div>

        <div
          className={`
            rounded-2xl
            p-8
            border
            shadow-lg
            ${
              darkMode
                ? "bg-gray-900 border-gray-800"
                : "bg-white border-gray-200"
            }
          `}
        >

          <form
            onSubmit={handleSubmit}
            className="space-y-6"
          >

            <div>
              <label className="block mb-2 font-medium">
                Workflow ID
              </label>

              <input
                type="number"
                name="workflow_id"
                value={formData.workflow_id}
                onChange={handleChange}
                required
                className={`
                  w-full p-3 rounded-xl border
                  ${
                    darkMode
                      ? "bg-gray-800 border-gray-700 text-white"
                      : "bg-white border-gray-300"
                  }
                `}
              />
            </div>

            <div>
              <label className="block mb-2 font-medium">
                Organization ID
              </label>

              <input
                type="number"
                name="organization_id"
                value={formData.organization_id}
                onChange={handleChange}
                required
                className={`
                  w-full p-3 rounded-xl border
                  ${
                    darkMode
                      ? "bg-gray-800 border-gray-700 text-white"
                      : "bg-white border-gray-300"
                  }
                `}
              />
            </div>

            <div>
              <label className="block mb-2 font-medium">
                Triggered By
              </label>

              <input
                type="text"
                name="triggered_by"
                value={formData.triggered_by}
                onChange={handleChange}
                required
                placeholder="admin"
                className={`
                  w-full p-3 rounded-xl border
                  ${
                    darkMode
                      ? "bg-gray-800 border-gray-700 text-white"
                      : "bg-white border-gray-300"
                  }
                `}
              />
            </div>

            <div>
              <label className="block mb-2 font-medium">
                Execution Context
              </label>

              <textarea
                rows="4"
                name="execution_context"
                value={formData.execution_context}
                onChange={handleChange}
                placeholder="Forecast approval request..."
                className={`
                  w-full p-3 rounded-xl border
                  ${
                    darkMode
                      ? "bg-gray-800 border-gray-700 text-white"
                      : "bg-white border-gray-300"
                  }
                `}
              />
            </div>

            <div className="flex justify-end gap-4">

              <button
                type="button"
                onClick={() =>
                  navigate("/workflow")
                }
                className="
                  px-6 py-3 rounded-xl
                  bg-gray-500 text-white
                  hover:bg-gray-600
                "
              >
                Cancel
              </button>

              <button
                type="submit"
                className="
                  px-6 py-3 rounded-xl
                  bg-green-600 text-white
                  hover:bg-green-700
                "
              >
                Execute Workflow
              </button>

            </div>

          </form>

        </div>

      </div>

    </Layout>
  );
}

export default Execute_Workflow;