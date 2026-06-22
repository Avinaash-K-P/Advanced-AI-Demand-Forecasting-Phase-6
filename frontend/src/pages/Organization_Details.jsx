import Layout from "../components/Layout";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import api from "../services/api";
import { toast } from "react-toastify";

function Organization_Details() {

  const navigate = useNavigate();

  const darkMode = localStorage.getItem("theme") === "dark";

  const [editMode, setEditMode] = useState(false);
  const { id } = useParams();

  const [organization, setOrganization] = useState(null);
  
  const [loading, setLoading] =
  useState(true);  

  const fetchOrganization = async () => {
  try {

    const response = await api.get(
      `/organizations/${id}`
    );

    setOrganization(response.data.data);

  } catch (error) {

    console.error(
      "Failed to fetch organization",
      error
    );

  } finally {

    setLoading(false);

  }
};

const handleUpdate = async () => {

  try {

    await api.put(
      `/organizations/${organization.id}`,
      {
        name: organization.name,
        industry: organization.industry,
        description: organization.description,
        contact_email: organization.contact_email,
        contact_phone: organization.contact_phone,
        address: organization.address,
        country: organization.country,
      }
    );

    toast.success("Organization updated");

    setEditMode(false);

  } catch (error) {

    console.error(error);

  }
};

const handleDelete = async () => {

  const confirmDelete = window.confirm(
    "Are you sure you want to delete this organization?"
  );

  if (!confirmDelete) return;

  try {

    await api.delete(
      `/organizations/${organization.id}`
    );

    toast.success(
      "Organization deleted successfully"
    );

    navigate("/admin/organization");

  } catch (error) {

    console.error(error);

  }
};


useEffect(() => {
  fetchOrganization();
}, [id]);

if (loading) {
  return (
    <Layout>
      <div className="p-8">
        Loading organization...
      </div>
    </Layout>
  );
}

if (!organization) {
  return (
    <Layout>
      <div className="p-8">
        Organization not found.
      </div>
    </Layout>
  );
}

  return (
    <Layout>
      <div className="p-8">

        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold">
            Organization Details
          </h1>

          <p
            className={`mt-2 ${
              darkMode
                ? "text-gray-400"
                : "text-gray-500"
            }`}
          >
            View organization profile and contact information.
          </p>
        </div>

        {/* Organization Information */}
        <div
          className={`
            rounded-2xl p-6 mb-6 border shadow-lg
            ${
              darkMode
                ? "bg-gray-900 border-gray-800"
                : "bg-white border-gray-200"
            }
          `}
        >
          <h2 className="text-xl font-semibold mb-4">
            Organization Information
          </h2>

          <div className="grid md:grid-cols-2 gap-4">

            <div>
              <p className="font-semibold">
                Organization Name
              </p>
              <p>{organization.name}</p>
            </div>

            <div>
              <p className="font-semibold">
                Organization Code
              </p>
              <p>{organization.code}</p>
            </div>

            <div>
              <p className="font-semibold">
                Industry
              </p>
              <p>{organization.industry}</p>
            </div>

            <div>
              <p className="font-semibold">
                Country
              </p>
              <p>{organization.country}</p>
            </div>

          </div>
        </div>

        {/* Contact Information */}
        <div
          className={`
            rounded-2xl p-6 mb-6 border shadow-lg
            ${
              darkMode
                ? "bg-gray-900 border-gray-800"
                : "bg-white border-gray-200"
            }
          `}
        >
          <h2 className="text-xl font-semibold mb-4">
            Contact Information
          </h2>

          <div className="grid md:grid-cols-2 gap-4">

            <div>
              <p className="font-semibold">
                Contact Email
              </p>
              <p>{organization.contact_email}</p>
            </div>

            <div>
              <p className="font-semibold">
                Contact Phone
              </p>
              <p>{organization.contact_phone}</p>
            </div>

          </div>

          <div className="mt-4">
            <p className="font-semibold">
              Address
            </p>
            <p>{organization.address}</p>
          </div>
        </div>

        {/* Description */}
        <div
          className={`
            rounded-2xl p-6 border shadow-lg
            ${
              darkMode
                ? "bg-gray-900 border-gray-800"
                : "bg-white border-gray-200"
            }
          `}
        >
          <h2 className="text-xl font-semibold mb-4">
            Description
          </h2>

          <p
            className={
              darkMode
                ? "text-gray-300"
                : "text-gray-700"
            }
          >
            {organization.description}
          </p>
        </div>

        {/* Actions */}
        <div className="flex justify-end gap-4 mt-8">

  <button
    onClick={() =>
      navigate("/admin/organization")
    }
    className="
      px-6 py-3 rounded-xl
      bg-gray-500 text-white
    "
  >
    Back
  </button>

  {!editMode ? (
    <>
      <button
        onClick={() =>
          setEditMode(true)
        }
        className="
          px-6 py-3 rounded-xl
          bg-blue-600 text-white
        "
      >
        Edit
      </button>

      <button
        onClick={handleDelete}
        className="
          px-6 py-3 rounded-xl
          bg-red-600 text-white
        "
      >
        Delete
      </button>
    </>
  ) : (
    <>
      <button
        onClick={() =>
          setEditMode(false)
        }
        className="
          px-6 py-3 rounded-xl
          bg-gray-600 text-white
        "
      >
        Cancel
      </button>

      <button
        onClick={handleUpdate}
        className="
          px-6 py-3 rounded-xl
          bg-green-600 text-white
        "
      >
        Save Changes
      </button>
    </>
  )}

{
  editMode ? (
    <input
      type="text"
      value={organization.name}
      onChange={(e) =>
        setOrganization({
          ...organization,
          name: e.target.value,
        })
      }
      className={`
        w-full p-2 rounded border
        ${
          darkMode
            ? "bg-gray-800 border-gray-700"
            : "bg-white border-gray-300"
        }
      `}
    />
  ) : (
    <p>{organization.name}</p>
  )
}



</div>

      </div>

    </Layout>
  );
}

export default Organization_Details;