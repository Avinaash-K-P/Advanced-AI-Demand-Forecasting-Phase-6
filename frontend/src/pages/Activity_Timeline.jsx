import Layout from "../components/Layout";
import { useEffect, useState } from "react";
import api from "../services/api";
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";

function Activity_Timeline() {

    const darkMode = localStorage.getItem("theme") === "dark";    
    const navigate = useNavigate();
    const [activities, setActivities] =
  useState([]);

const [loading, setLoading] =
  useState(false);

  const fetchActivities = async () => {

  try {

    setLoading(true);

    const response = await api.get(
      "/governance/activity-timeline"
    );

    setActivities(
      response.data.data
    );

  } catch (error) {

    console.error(error);

    toast.error(
      "Failed to load activity timeline"
    );

  } finally {

    setLoading(false);

  }

};
useEffect(() => {
  fetchActivities();
}, []);

    return(
        <Layout>
            <div className="mb-8">

  <h1 className="text-3xl font-bold">
    Activity Timeline
  </h1>

  <p
    className={`mt-2 ${
      darkMode
        ? "text-gray-400"
        : "text-gray-500"
    }`}
  >
    Monitor forecast activities,
    lifecycle updates, and user actions.
  </p>

</div>
{
  loading && (
    <div className="mb-6">
      Loading activity timeline...
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
          Forecast ID
        </th>

        <th className="p-4 text-left">
          Action
        </th>

        <th className="p-4 text-left">
          Category
        </th>

        <th className="p-4 text-left">
          Description
        </th>

        <th className="p-4 text-left">
          Timestamp
        </th>

      </tr>

    </thead>

    <tbody>

      {activities.length > 0 ? (

        activities.map((activity) => (

          <tr
            key={activity.id}
            className="border-t"
          >

            <td className="p-4">
              {activity.forecast_id}
            </td>

            <td className="p-4">
              {activity.action}
            </td>

            <td className="p-4">
              {activity.category}
            </td>

            <td className="p-4">
              {activity.description}
            </td>

            <td className="p-4">
              {activity.timestamp}
            </td>

          </tr>

        ))

      ) : (

        <tr>

          <td
            colSpan="5"
            className="
              p-6
              text-center
            "
          >
            No activity records found
          </td>

        </tr>

      )}

    </tbody>

  </table>

</div>

<div className="mt-6">

  <button
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

export default Activity_Timeline