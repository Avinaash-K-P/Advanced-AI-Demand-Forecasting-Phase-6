import Layout from "../components/Layout";
import { useEffect, useState } from "react";
import api from "../services/api";
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";

function Forecast_Versions() {

const darkMode = localStorage.getItem("theme") === "dark";    

const navigate = useNavigate();

const [forecastDate, setForecastDate] =
  useState("");

const [versions, setVersions] =
  useState([]);

const [loading, setLoading] =
  useState(false);

const fetchVersions = async () => {

  if (!forecastDate) {

    toast.error(
      "Please select forecast date"
    );

    return;

  }

  try {

    setLoading(true);

    const response = await api.get(
      `/governance/versions/${forecastDate}`
    );

    setVersions(
      response.data.data
    );

  } catch (error) {

    console.error(error);

    toast.error(
      "Failed to fetch versions"
    );

  } finally {

    setLoading(false);

  }

};  

    return (
        <Layout>
            <div className="mb-8">

  <h1 className="text-3xl font-bold">
    Forecast Versions
  </h1>

  <p
    className={`mt-2 ${
      darkMode
        ? "text-gray-400"
        : "text-gray-500"
    }`}
  >
    Track forecast revision history
    and version changes.
  </p>

</div>

<div
  className={`
    p-6 rounded-2xl border mb-6
    ${
      darkMode
        ? "bg-gray-900 border-gray-800"
        : "bg-white border-gray-200"
    }
  `}
>

  <label className="block mb-2 font-medium">
    Forecast Date
  </label>

  <input
    type="date"
    value={forecastDate}
    onChange={(e) =>
      setForecastDate(
        e.target.value
      )
    }
    className={`
      w-full p-3 rounded-xl border
      ${
        darkMode
          ? "bg-gray-800 border-gray-700"
          : "bg-white border-gray-300"
      }
    `}
  />

  <button
    onClick={fetchVersions}
    className="
      mt-4
      px-6 py-3
      rounded-xl
      bg-blue-600
      text-white
      hover:bg-blue-700
    "
  >
    Search Versions
  </button>

</div>

{
  loading && (
    <div className="mb-6">
      Loading revisions...
    </div>
  )
}
<div
  className={`
    rounded-2xl
    border
    overflow-hidden
    ${
      darkMode
        ? "bg-gray-900 border-gray-800"
        : "bg-white border-gray-200"
    }
  `}
>

  <table className="w-full">

    <thead>

      <tr
        className={
          darkMode
            ? "bg-gray-800"
            : "bg-gray-100"
        }
      >

        <th className="p-4 text-left">
          Revision
        </th>

        <th className="p-4 text-left">
          Forecast Date
        </th>

        <th className="p-4 text-left">
          Created By
        </th>

        <th className="p-4 text-left">
          Created At
        </th>

      </tr>

    </thead>

    <tbody>

      {versions.length > 0 ? (

        versions.map((version) => (

          <tr
            key={version.id}
            className="border-t"
          >

            <td className="p-4">
              {version.revision_number}
            </td>

            <td className="p-4">
              {version.forecast_date}
            </td>

            <td className="p-4">
              {version.created_by}
            </td>

            <td className="p-4">
              {version.created_at}
            </td>

          </tr>

        ))

      ) : (

        <tr>

          <td
            colSpan="4"
            className="
              p-6
              text-center
            "
          >
            No forecast revisions found
          </td>

        </tr>

      )}

    </tbody>

  </table>

</div>

<button
  onClick={() =>
    navigate("/governance")
  }
  className="
    mt-6
    px-6 py-3
    rounded-xl
    bg-gray-500
    text-white
  "
>
  Back
</button>

        </Layout>
    )
}

export default Forecast_Versions;