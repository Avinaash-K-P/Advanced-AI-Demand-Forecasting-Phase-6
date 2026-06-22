import Layout from "../components/Layout";
import { useEffect, useState } from "react";
import api from "../services/api";
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";

function Forecast_Lifecycle() {

    const darkMode = localStorage.getItem("theme") === "dark";    
    const navigate = useNavigate();

    const [formData, setFormData] =
  useState({
    forecast_id: "",
    status: "",
    performed_by: "",
  });

const [loading, setLoading] =
  useState(false);
    
  const handleChange = (e) => {

  setFormData({
    ...formData,
    [e.target.name]:
      e.target.value,
  });

};

const handleSubmit = async (e) => {

  e.preventDefault();

  try {

    setLoading(true);

    await api.put(
      "/governance/lifecycle",
      formData
    );

    toast.success(
      "Lifecycle updated successfully"
    );

    setFormData({
      forecast_id: "",
      status: "",
      performed_by: "",
    });

  } catch (error) {

    console.error(error);

    toast.error(
      "Failed to update lifecycle"
    );

  } finally {

    setLoading(false);

  }

};

    return(
        <Layout>
            <div className="mb-8">

  <h1 className="text-3xl font-bold">
    Forecast Lifecycle
  </h1>

  <p
    className={`mt-2 ${
      darkMode
        ? "text-gray-400"
        : "text-gray-500"
    }`}
  >
    Manage forecast approval stages
    and lifecycle transitions.
  </p>

</div>

<div className="mb-5">

  <label className="block mb-2">
    Forecast ID
  </label>

  <input
    type="number"
    name="forecast_id"
    value={formData.forecast_id}
    onChange={handleChange}
    required
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

<div className="mb-5">

  <label className="block mb-2">
    Status
  </label>

  <select
    name="status"
    value={formData.status}
    onChange={handleChange}
    required
    className={`
      w-full p-3 rounded-xl border
      ${
        darkMode
          ? "bg-gray-800 border-gray-700"
          : "bg-white border-gray-300"
      }
    `}
  >

    <option value="">
      Select Status
    </option>

    <option value="Draft">
      Draft
    </option>

    <option value="Submitted">
      Submitted
    </option>

    <option value="Under Review">
      Under Review
    </option>

    <option value="Approved">
      Approved
    </option>

    <option value="Rejected">
      Rejected
    </option>

  </select>

</div>

<div className="mb-5">

  <label className="block mb-2">
    Performed By
  </label>

  <input
    type="text"
    name="performed_by"
    value={formData.performed_by}
    onChange={handleChange}
    required
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

<div className="flex gap-4">

  <button
    type="submit"
    disabled={loading}
    className="
      px-6 py-3
      rounded-xl
      bg-blue-600
      text-white
      hover:bg-blue-700
    "
  >
    {
      loading
      ? "Updating..."
      : "Update Lifecycle"
    }
  </button>

  <button
    type="button"
    onClick={() =>
      navigate("/governance")
    }
    className="
      px-6 py-3
      rounded-xl
      bg-gray-500
      text-white
    "
  >
    Back
  </button>

</div>

        </Layout>
    )

}

export default Forecast_Lifecycle;
