import Layout from "../components/Layout";
import { useEffect, useState } from "react";
import api from "../services/api";
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";

function Audit_Logs() {

    const darkMode = localStorage.getItem("theme") === "dark";    
    const navigate = useNavigate();

    const [auditLogs, setAuditLogs] = useState([]);

    const [loading, setLoading] = useState(false);

    const fetchAuditLogs = async () => {

  try {

    setLoading(true);

    const response = await api.get(
      "/governance/audit-logs"
    );

    setAuditLogs(
      response.data.data
    );

  } catch (error) {

    console.error(error);

    toast.error(
      "Failed to load audit logs"
    );

  } finally {

    setLoading(false);

  }

};

useEffect(() => {
  fetchAuditLogs();
}, []);

    return(
        <Layout>
            <div className="mb-8">

  <h1 className="text-3xl font-bold">
    Governance Audit Logs
  </h1>

  <p
    className={`mt-2 ${
      darkMode
        ? "text-gray-400"
        : "text-gray-500"
    }`}
  >
    Review governance changes,
    approval actions, and forecast updates.
  </p>

</div>

{
  loading && (
    <div className="mb-6">
      Loading audit logs...
    </div>
  )
}

<div
  className={`
    rounded-2xl
    border
    overflow-x-auto
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
          Organization
        </th>

        <th className="p-4 text-left">
          Entity Type
        </th>

        <th className="p-4 text-left">
          Entity ID
        </th>

        <th className="p-4 text-left">
          Action
        </th>

        <th className="p-4 text-left">
          Performed By
        </th>

        <th className="p-4 text-left">
          Old Value
        </th>

        <th className="p-4 text-left">
          New Value
        </th>

        <th className="p-4 text-left">
          Created At
        </th>

      </tr>

    </thead>

    <tbody>

      {auditLogs.length > 0 ? (

        auditLogs.map((log) => (

          <tr
            key={log.id}
            className="border-t"
          >

            <td className="p-4">
              {log.organization_id}
            </td>

            <td className="p-4">
              {log.entity_type}
            </td>

            <td className="p-4">
              {log.entity_id}
            </td>

            <td className="p-4">
              {log.action}
            </td>

            <td className="p-4">
              {log.performed_by}
            </td>

            <td className="p-4">
              {log.old_value}
            </td>

            <td className="p-4">
              {log.new_value}
            </td>

            <td className="p-4">
              {log.created_at}
            </td>

          </tr>

        ))

      ) : (

        <tr>

          <td
            colSpan="8"
            className="
              p-6
              text-center
            "
          >
            No audit logs found
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

    );
}

export default Audit_Logs;