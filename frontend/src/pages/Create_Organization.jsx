import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Layout from "../components/Layout";
import api from "../services/api";
import { toast } from "react-toastify";

function Create_Organization() {

  const navigate = useNavigate();

  const darkMode =
    localStorage.getItem("theme") === "dark";

  const [formData, setFormData] = useState({
    name: "",
    code: "",
    industry: "",
    description: "",
    contact_email: "",
    contact_phone: "",
    address: "",
    country: "",
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
      "organizations/",
      formData
    );

    console.log(response.data);

    toast.success("Organization created successfully");

    navigate("/organization");

  } catch (error) {

    console.error(error);

    toast.error(
      error?.response?.data?.message ||
      "Failed to create organization"
    );
  }
};




  return (
    <Layout>
      <div className="p-8">

        <div className="mb-8">
          <h1 className="text-3xl font-bold">
            Create Organization
          </h1>

          <p
            className={`mt-2 ${
              darkMode
                ? "text-gray-400"
                : "text-gray-500"
            }`}
          >
            Register a new organization and
            define its profile information.
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

            <div className="grid md:grid-cols-2 gap-6">

              <div>
                <label className="block mb-2 font-medium">
                  Organization Name *
                </label>

                <input
                  type="text"
                  name="name"
                  required
                  value={formData.name}
                  onChange={handleChange}
                  className={`
                    w-full p-3 rounded-xl border
                    ${
                      darkMode
                        ? "bg-gray-800 border-gray-700"
                        : "bg-white border-gray-300"
                    }
                  `}
                />
              </div>

              <div>
                <label className="block mb-2 font-medium">
                  Organization Code *
                </label>

                <input
                  type="text"
                  name="code"
                  required
                  value={formData.code}
                  onChange={handleChange}
                  className={`
                    w-full p-3 rounded-xl border
                    ${
                      darkMode
                        ? "bg-gray-800 border-gray-700"
                        : "bg-white border-gray-300"
                    }
                  `}
                />
              </div>

            </div>

            <div className="grid md:grid-cols-2 gap-6">

              <div>
                <label className="block mb-2 font-medium">
                  Industry
                </label>

                <input
                  type="text"
                  name="industry"
                  value={formData.industry}
                  onChange={handleChange}
                  className={`
                    w-full p-3 rounded-xl border
                    ${
                      darkMode
                        ? "bg-gray-800 border-gray-700"
                        : "bg-white border-gray-300"
                    }
                  `}
                />
              </div>

              <div>
                <label className="block mb-2 font-medium">
                  Country
                </label>

                <input
                  type="text"
                  name="country"
                  value={formData.country}
                  onChange={handleChange}
                  className={`
                    w-full p-3 rounded-xl border
                    ${
                      darkMode
                        ? "bg-gray-800 border-gray-700"
                        : "bg-white border-gray-300"
                    }
                  `}
                />
              </div>

            </div>

            <div className="grid md:grid-cols-2 gap-6">

              <div>
                <label className="block mb-2 font-medium">
                  Contact Email
                </label>

                <input
                  type="email"
                  name="contact_email"
                  value={formData.contact_email}
                  onChange={handleChange}
                  className={`
                    w-full p-3 rounded-xl border
                    ${
                      darkMode
                        ? "bg-gray-800 border-gray-700"
                        : "bg-white border-gray-300"
                    }
                  `}
                />
              </div>

              <div>
                <label className="block mb-2 font-medium">
                  Contact Phone
                </label>

                <input
                  type="text"
                  name="contact_phone"
                  value={formData.contact_phone}
                  onChange={handleChange}
                  className={`
                    w-full p-3 rounded-xl border
                    ${
                      darkMode
                        ? "bg-gray-800 border-gray-700"
                        : "bg-white border-gray-300"
                    }
                  `}
                />
              </div>

            </div>

            <div>
              <label className="block mb-2 font-medium">
                Address
              </label>

              <textarea
                rows="3"
                name="address"
                value={formData.address}
                onChange={handleChange}
                className={`
                  w-full p-3 rounded-xl border
                  ${
                    darkMode
                      ? "bg-gray-800 border-gray-700"
                      : "bg-white border-gray-300"
                  }
                `}
              />
            </div>

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
                      ? "bg-gray-800 border-gray-700"
                      : "bg-white border-gray-300"
                  }
                `}
              />
            </div>

            <div className="flex justify-end gap-4">

              <button
                type="button"
                onClick={() =>
                  navigate("/admin/organization")
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
                Create Organization
              </button>

            </div>

          </form>
        </div>

      </div>
    </Layout>
  );
}

export default Create_Organization;