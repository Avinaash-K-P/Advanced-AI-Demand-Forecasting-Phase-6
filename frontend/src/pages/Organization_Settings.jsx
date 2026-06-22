import Layout from "../components/Layout";
import { useEffect, useState } from "react";
import api from "../services/api";

function Organization_Settings() {

  const darkMode =
    localStorage.getItem("theme") === "dark";

const organizationId = 1; // Replace later with actual organization

const [settingsId, setSettingsId] = useState(null);

const [loading, setLoading] = useState(false);

const [settings, setSettings] = useState({
  organization_id: organizationId,
  timezone: "UTC",
  currency: "USD",
  forecast_retention_days: 365,
  default_forecast_model: "",
  notifications_enabled: true,
});

const fetchSettings = async () => {

  try {

    const response = await api.get(
      `/organizations-settings/${settingsId}`
    );

    const data = response.data.data;

    setSettings({
      organization_id: data.organization_id,
      timezone: data.timezone,
      currency: data.currency,
      forecast_retention_days:
        data.forecast_retention_days,
      default_forecast_model:
        data.default_forecast_model || "",
      notifications_enabled:
        data.notifications_enabled,
    });

  } catch (error) {

    console.error(
      "Failed to load settings",
      error
    );

  }
};

const createSettings = async () => {

  try {

    await api.post(
      "/organizations-settings/",
      settings
    );

    alert(
      "Organization settings created successfully"
    );

  } catch (error) {

    console.error(error);

    alert(
      error?.response?.data?.message ||
      "Failed to create settings"
    );
  }
};

const updateSettings = async () => {

  try {

    await api.put(
      `/organizations-settings/${settingsId}`,
      {
        timezone: settings.timezone,
        currency: settings.currency,
        forecast_retention_days:
          settings.forecast_retention_days,
        default_forecast_model:
          settings.default_forecast_model,
        notifications_enabled:
          settings.notifications_enabled,
      }
    );

    alert(
      "Organization settings updated successfully"
    );

  } catch (error) {

    console.error(error);

    alert(
      error?.response?.data?.message ||
      "Failed to update settings"
    );
  }
};


  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;

    setSettings((prev) => ({
      ...prev,
      [name]:
        type === "checkbox"
          ? checked
          : value,
    }));
  };

const handleSubmit = async (e) => {

  e.preventDefault();

  setLoading(true);

  try {

    if (settingsId) {

      await updateSettings();

    } else {

      await createSettings();

    }

  } finally {

    setLoading(false);

  }
};

  return (
    <Layout>
      <div className="p-8">

        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold">
            Organization Settings
          </h1>

          <p
            className={`mt-2 ${
              darkMode
                ? "text-gray-400"
                : "text-gray-500"
            }`}
          >
            Configure forecasting and operational preferences.
          </p>
        </div>

        <form
          onSubmit={handleSubmit}
          className="space-y-6"
        >

          {/* Regional Settings */}
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
            <h2 className="text-xl font-semibold mb-6">
              Regional Settings
            </h2>

            <div className="grid md:grid-cols-2 gap-6">

              <div>
                <label className="block mb-2 font-medium">
                  Timezone
                </label>

                <select
                  name="timezone"
                  value={settings.timezone}
                  onChange={handleChange}
                  className={`
                    w-full p-3 rounded-xl border
                    ${
                      darkMode
                        ? "bg-gray-800 border-gray-700"
                        : "bg-white border-gray-300"
                    }
                  `}
                >
                  <option>UTC</option>
                  <option>Asia/Kolkata</option>
                  <option>America/New_York</option>
                  <option>Europe/London</option>
                </select>
              </div>

              <div>
                <label className="block mb-2 font-medium">
                  Currency
                </label>

                <select
                  name="currency"
                  value={settings.currency}
                  onChange={handleChange}
                  className={`
                    w-full p-3 rounded-xl border
                    ${
                      darkMode
                        ? "bg-gray-800 border-gray-700"
                        : "bg-white border-gray-300"
                    }
                  `}
                >
                  <option>USD</option>
                  <option>INR</option>
                  <option>EUR</option>
                  <option>GBP</option>
                </select>
              </div>

            </div>
          </div>

          {/* Forecast Configuration */}
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
            <h2 className="text-xl font-semibold mb-6">
              Forecast Configuration
            </h2>

            <div className="grid md:grid-cols-2 gap-6">

              <div>
                <label className="block mb-2 font-medium">
                  Forecast Retention Days
                </label>

                <input
                  type="number"
                  name="forecast_retention_days"
                  value={
                    settings.forecast_retention_days
                  }
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
                  Default Forecast Model
                </label>

                <select
                  name="default_forecast_model"
                  value={
                    settings.default_forecast_model
                  }
                  onChange={handleChange}
                  className={`
                    w-full p-3 rounded-xl border
                    ${
                      darkMode
                        ? "bg-gray-800 border-gray-700"
                        : "bg-white border-gray-300"
                    }
                  `}
                >
                  <option>Prophet</option>
                  <option>ARIMA</option>
                  <option>LSTM</option>
                  <option>XGBoost</option>
                  <option>Random Forest</option>
                </select>
              </div>

            </div>
          </div>

          {/* Notifications */}
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
            <h2 className="text-xl font-semibold mb-6">
              Notification Preferences
            </h2>

            <label className="flex items-center gap-3">
              <input
                type="checkbox"
                name="notifications_enabled"
                checked={
                  settings.notifications_enabled
                }
                onChange={handleChange}
                className="w-5 h-5"
              />

              <span>
                Enable Notifications
              </span>
            </label>
          </div>

          {/* Save Button */}
          <div className="flex justify-end">

<button
  type="submit"
  disabled={loading}
  className="
    px-6 py-3
    bg-green-600
    hover:bg-green-700
    text-white
    rounded-xl
    disabled:opacity-50
  "
>
  {loading
    ? "Saving..."
    : "Save Settings"}
</button>

          </div>

        </form>

      </div>
    </Layout>
  );
}

export default Organization_Settings;