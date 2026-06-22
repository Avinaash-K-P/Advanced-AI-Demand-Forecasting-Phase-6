import Layout from "../components/Layout";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import { toast } from "react-toastify";

function Create_Workflow() {

  const navigate = useNavigate();

  const darkMode =
    localStorage.getItem("theme") === "dark";

  const [formData, setFormData] = useState({
    organization_id: "",
    name: "",
    description: "",
    workflow_type: "",
    trigger_event: "",
    is_active: true,
    created_by: "",
  });

  const handleChange = (e) => {

    const { name, value, type, checked } =
      e.target;

    setFormData({
      ...formData,
      [name]:
        type === "checkbox"
          ? checked
          : value,
    });
  };

const handleSubmit = async (e) => {

  e.preventDefault();

  try {

    const payload = {
      organization_id: Number(
        formData.organization_id
      ),
      name: formData.name,
      description: formData.description,
      workflow_type: formData.workflow_type,
      trigger_event: formData.trigger_event,
      is_active: formData.is_active,
      created_by: formData.created_by,
    };

    const response = await api.post(
      "/workflow/",
      payload
    );

    console.log(response.data);

    toast.success(
      "Workflow created successfully"
    );

    navigate("/workflow/view");

  } catch (error) {

    console.error(error);

    toast.error(
      error?.response?.data?.message ||
      "Failed to create workflow"
    );
  }
};

  return (
    <Layout>
      <div className="p-8 max-w-4xl mx-auto">

        {/* Header */}
        <div className="mb-8">

          <h1 className="text-3xl font-bold">
            Create Workflow
          </h1>

          <p
            className={`mt-2 ${
              darkMode
                ? "text-gray-400"
                : "text-gray-500"
            }`}
          >
            Create a workflow automation process
            for approvals and business operations.
          </p>

        </div>

        {/* Form Card */}
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

            {/* Organization ID */}
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

            {/* Workflow Name */}
            <div>
              <label className="block mb-2 font-medium">
                Workflow Name
              </label>

              <input
                type="text"
                name="name"
                value={formData.name}
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

            {/* Description */}
            <div>
              <label className="block mb-2 font-medium">
                Description
              </label>

              <textarea
                rows="4"
                name="description"
                value={formData.description}
                onChange={handleChange}
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

            {/* Workflow Type */}
            <div>
              <label className="block mb-2 font-medium">
                Workflow Type
              </label>

              <input
                type="text"
                name="workflow_type"
                value={formData.workflow_type}
                onChange={handleChange}
                required
                placeholder="Approval, Forecast, Review..."
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

            {/* Trigger Event */}
            <div>
              <label className="block mb-2 font-medium">
                Trigger Event
              </label>

              <input
                type="text"
                name="trigger_event"
                value={formData.trigger_event}
                onChange={handleChange}
                required
                placeholder="Forecast Submitted"
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

            {/* Created By */}
            <div>
              <label className="block mb-2 font-medium">
                Created By
              </label>

              <input
                type="text"
                name="created_by"
                value={formData.created_by}
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

            {/* Active Checkbox */}
            <div className="flex items-center gap-3">

              <input
                type="checkbox"
                name="is_active"
                checked={formData.is_active}
                onChange={handleChange}
              />

              <label>
                Active Workflow
              </label>

            </div>

            {/* Buttons */}
            <div className="flex justify-end gap-4 pt-4">

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
                Create Workflow
              </button>

            </div>

          </form>

        </div>

      </div>
    </Layout>
  );
}

export default Create_Workflow;