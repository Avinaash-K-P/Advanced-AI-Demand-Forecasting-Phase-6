import Layout from "../components/Layout";
import { useState } from "react";
import api from "../services/api";
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";

function Create_Business_Target() {

  const navigate = useNavigate();

  const darkMode =
    localStorage.getItem("theme") === "dark";

  const [formData, setFormData] = useState({
    organization_id: "",
    annual_plan_id: "",
    quarterly_plan_id: "",
    target_name: "",
    target_type: "",
    target_value: "",
    current_value: 0,
    unit: "",
    status: "Active",
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

    const response = await api.post(
      "/planning/targets",
      {
        ...formData,
        target_value: Number(formData.target_value),
        current_value: Number(formData.current_value),
      }
    );

    console.log(response.data);

    toast.success(
      "Business Target Created Successfully"
    );

    navigate("/planning");

  } catch (error) {

    console.error(error);

    toast.error(
      error?.response?.data?.message ||
      "Failed to create business target"
    );

  }

};

  return (
    <Layout>

      <div className="p-8 max-w-5xl mx-auto">

        <h1 className="text-3xl font-bold mb-2">
          Create Business Target
        </h1>

        <p
          className={`mb-8 ${
            darkMode
              ? "text-gray-400"
              : "text-gray-500"
          }`}
        >
          Define business objectives and measurable targets.
        </p>

        <form
          onSubmit={handleSubmit}
          className={`
            p-8 rounded-2xl border shadow-lg
            ${
              darkMode
                ? "bg-gray-900 border-gray-800"
                : "bg-white border-gray-200"
            }
          `}
        >

          <div className="grid md:grid-cols-2 gap-6">

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
                className="
                  w-full p-3 rounded-xl border
                  dark:bg-gray-800
                "
              />
            </div>

            {/* Annual Plan ID */}

            <div>
              <label className="block mb-2 font-medium">
                Annual Plan ID
              </label>

              <input
                type="number"
                name="annual_plan_id"
                value={formData.annual_plan_id}
                onChange={handleChange}
                required
                className="
                  w-full p-3 rounded-xl border
                  dark:bg-gray-800
                "
              />
            </div>

            {/* Quarterly Plan ID */}

            <div>
              <label className="block mb-2 font-medium">
                Quarterly Plan ID
              </label>

              <input
                type="number"
                name="quarterly_plan_id"
                value={formData.quarterly_plan_id}
                onChange={handleChange}
                required
                className="
                  w-full p-3 rounded-xl border
                  dark:bg-gray-800
                "
              />
            </div>

            {/* Target Name */}

            <div>
              <label className="block mb-2 font-medium">
                Target Name
              </label>

              <input
                type="text"
                name="target_name"
                value={formData.target_name}
                onChange={handleChange}
                required
                className="
                  w-full p-3 rounded-xl border
                  dark:bg-gray-800
                "
              />
            </div>

            {/* Target Type */}

            <div>
              <label className="block mb-2 font-medium">
                Target Type
              </label>

              <select
                name="target_type"
                value={formData.target_type}
                onChange={handleChange}
                required
                className="
                  w-full p-3 rounded-xl border
                  dark:bg-gray-800
                "
              >
                <option value="">
                  Select Type
                </option>

                <option value="Revenue">
                  Revenue
                </option>

                <option value="Demand">
                  Demand
                </option>

                <option value="Inventory">
                  Inventory
                </option>

                <option value="Sales">
                  Sales
                </option>

                <option value="Growth">
                  Growth
                </option>

              </select>
            </div>

            {/* Target Value */}

            <div>
              <label className="block mb-2 font-medium">
                Target Value
              </label>

              <input
                type="number"
                name="target_value"
                value={formData.target_value}
                onChange={handleChange}
                required
                className="
                  w-full p-3 rounded-xl border
                  dark:bg-gray-800
                "
              />
            </div>

            {/* Current Value */}

            <div>
              <label className="block mb-2 font-medium">
                Current Value
              </label>

              <input
                type="number"
                name="current_value"
                value={formData.current_value}
                onChange={handleChange}
                className="
                  w-full p-3 rounded-xl border
                  dark:bg-gray-800
                "
              />
            </div>

            {/* Unit */}

            <div>
              <label className="block mb-2 font-medium">
                Unit
              </label>

              <input
                type="text"
                name="unit"
                placeholder="Units, %, INR, USD"
                value={formData.unit}
                onChange={handleChange}
                required
                className="
                  w-full p-3 rounded-xl border
                  dark:bg-gray-800
                "
              />
            </div>

            {/* Status */}

            <div>
              <label className="block mb-2 font-medium">
                Status
              </label>

              <select
                name="status"
                value={formData.status}
                onChange={handleChange}
                className="
                  w-full p-3 rounded-xl border
                  dark:bg-gray-800
                "
              >
                <option value="Active">
                  Active
                </option>

                <option value="Completed">
                  Completed
                </option>

                <option value="Pending">
                  Pending
                </option>
              </select>
            </div>

          </div>

          <div className="flex justify-end gap-4 mt-8">

            <button
              type="button"
              onClick={() => navigate("/planning")}
              className="
                px-6 py-3 rounded-xl
                bg-gray-500 text-white
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
              Create Target
            </button>

          </div>

        </form>

      </div>

    </Layout>
  );
}

export default Create_Business_Target;