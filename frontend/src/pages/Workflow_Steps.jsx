import Layout from "../components/Layout";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import { toast } from "react-toastify";

function Create_Workflow_Step() {

  const navigate = useNavigate();

  const darkMode =
    localStorage.getItem("theme") === "dark";

  const [formData, setFormData] = useState({
    workflow_id: "",
    step_order: "",
    step_name: "",
    step_type: "",
    configuration: "",
    is_required: "Yes",
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
      workflow_id: Number(formData.workflow_id),
      step_order: formData.step_order,
      step_name: formData.step_name,
      step_type: formData.step_type,
      configuration: formData.configuration,
      is_required: formData.is_required,
    };

    const response = await api.post(
      "/workflow/steps",
      payload
    );

    console.log(response.data);

    toast.success(
      "Workflow step created successfully"
    );

    setFormData({
      workflow_id: "",
      step_order: "",
      step_name: "",
      step_type: "",
      configuration: "",
      is_required: "Yes",
    });

    navigate("/workflow/view");

  } catch (error) {

    console.error(error);

    toast.error(
      error?.response?.data?.message ||
      "Failed to create workflow step"
    );
  }
};

  return (
    <Layout>

      <div className="p-8 max-w-4xl mx-auto">

        <div className="mb-8">

          <h1 className="text-3xl font-bold">
            Create Workflow Step
          </h1>

          <p
            className={`mt-2 ${
              darkMode
                ? "text-gray-400"
                : "text-gray-500"
            }`}
          >
            Configure workflow approval and automation steps.
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
                Step Order
              </label>

              <input
                type="text"
                name="step_order"
                value={formData.step_order}
                onChange={handleChange}
                required
                placeholder="1"
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
                Step Name
              </label>

              <input
                type="text"
                name="step_name"
                value={formData.step_name}
                onChange={handleChange}
                required
                placeholder="Manager Approval"
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
                Step Type
              </label>

              <input
                type="text"
                name="step_type"
                value={formData.step_type}
                onChange={handleChange}
                required
                placeholder="Approval"
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
                Configuration
              </label>

              <textarea
                rows="3"
                name="configuration"
                value={formData.configuration}
                onChange={handleChange}
                placeholder="Manager Role"
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
                Required
              </label>

              <select
                name="is_required"
                value={formData.is_required}
                onChange={handleChange}
                className={`
                  w-full p-3 rounded-xl border
                  ${
                    darkMode
                      ? "bg-gray-800 border-gray-700 text-white"
                      : "bg-white border-gray-300"
                  }
                `}
              >
                <option value="Yes">
                  Yes
                </option>

                <option value="No">
                  No
                </option>
              </select>
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
                Create Step
              </button>

            </div>

          </form>

        </div>

      </div>

    </Layout>
  );
}

export default Create_Workflow_Step;