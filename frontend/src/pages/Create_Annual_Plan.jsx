import Layout from "../components/Layout";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import { toast } from "react-toastify";

function Create_Annual_Plan() {

  const navigate = useNavigate();

  const darkMode =
    localStorage.getItem("theme") === "dark";

  const [formData, setFormData] = useState({
    organization_id: "",
    year: "",
    name: "",
    description: "",
    status: "Draft",
    created_by: "",
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
      "/planning/annual",
      formData
    );

    console.log(response.data);

    toast.success(
      "Annual Plan Created Successfully"
    );

    navigate("/planning");

  } catch (error) {

    console.error(error);

    toast.error(
      error?.response?.data?.message ||
      "Failed to create annual plan"
    );

  }

};

  return (
    <Layout>

      <div className="p-8 max-w-4xl mx-auto">

        <h1 className="text-3xl font-bold mb-2">
          Create Annual Plan
        </h1>

        <p
          className={`mb-8 ${
            darkMode
              ? "text-gray-400"
              : "text-gray-500"
          }`}
        >
          Create a strategic annual planning record
          for your organization.
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

            <div className="md:col-span-2">
              <label className="block mb-2 font-medium">
                Created By
              </label>

              <input
                type="text"
                name="created_by"
                value={formData.created_by}
                onChange={handleChange}
                required
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
              Create Annual Plan
            </button>

          </div>

        </form>

      </div>

    </Layout>
  );
}

export default Create_Annual_Plan;