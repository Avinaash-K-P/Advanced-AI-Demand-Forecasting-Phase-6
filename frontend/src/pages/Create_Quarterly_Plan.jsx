import Layout from "../components/Layout";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import { toast } from "react-toastify";


function Create_Quarterly_Plan() {

  const navigate = useNavigate();

  const darkMode =
    localStorage.getItem("theme") === "dark";

  const [formData, setFormData] = useState({
    organization_id: "",
    annual_plan_id: "",
    quarter: "Q1",
    year: "",
    name: "",
    description: "",
    status: "Draft",
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
      "/planning/quarterly",
      formData
    );

    console.log(response.data);

    toast.success(
      "Quarterly Plan Created Successfully"
    );

    navigate("/planning");

  } catch (error) {

    console.error(error);

    toast.error(
      error?.response?.data?.message ||
      "Failed to create quarterly plan"
    );

  }

};

  return (
    <Layout>

      <div className="p-8 max-w-4xl mx-auto">

        <h1 className="text-3xl font-bold mb-2">
          Create Quarterly Plan
        </h1>

        <p
          className={`mb-8 ${
            darkMode
              ? "text-gray-400"
              : "text-gray-500"
          }`}
        >
          Create quarterly objectives linked to an annual plan.
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

            {/* Quarter */}

            <div>
              <label className="block mb-2 font-medium">
                Quarter
              </label>

              <select
                name="quarter"
                value={formData.quarter}
                onChange={handleChange}
                className="
                  w-full p-3 rounded-xl border
                  dark:bg-gray-800
                "
              >
                <option value="Q1">Q1</option>
                <option value="Q2">Q2</option>
                <option value="Q3">Q3</option>
                <option value="Q4">Q4</option>
              </select>
            </div>

            {/* Year */}

            <div>
              <label className="block mb-2 font-medium">
                Year
              </label>

              <input
                type="text"
                name="year"
                placeholder="2026"
                value={formData.year}
                onChange={handleChange}
                required
                className="
                  w-full p-3 rounded-xl border
                  dark:bg-gray-800
                "
              />
            </div>

            {/* Plan Name */}

            <div>
              <label className="block mb-2 font-medium">
                Plan Name
              </label>

              <input
                type="text"
                name="name"
                value={formData.name}
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
                <option value="Draft">
                  Draft
                </option>

                <option value="Active">
                  Active
                </option>

                <option value="Completed">
                  Completed
                </option>
              </select>
            </div>

            {/* Description */}

            <div className="md:col-span-2">

              <label className="block mb-2 font-medium">
                Description
              </label>

              <textarea
                rows="4"
                name="description"
                value={formData.description}
                onChange={handleChange}
                className="
                  w-full p-3 rounded-xl border
                  dark:bg-gray-800
                "
              />

            </div>

          </div>

          <div className="flex justify-end gap-4 mt-8">

            <button
              type="button"
              onClick={() =>
                navigate("/planning")
              }
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
              Create Quarterly Plan
            </button>

          </div>

        </form>

      </div>

    </Layout>
  );
}

export default Create_Quarterly_Plan;