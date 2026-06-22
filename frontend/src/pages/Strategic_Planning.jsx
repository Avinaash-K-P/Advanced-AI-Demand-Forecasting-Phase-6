import Layout from "../components/Layout";
import { useNavigate } from "react-router-dom";

function Strategic_Planning() {

  const navigate = useNavigate();

  const darkMode =
    localStorage.getItem("theme") === "dark";

  const cards = [

    {
      icon: "📅",
      title: "Annual Plans",
      description:
        "Create and manage annual strategic plans.",
      onClick: () =>
        navigate("/planning/annual"),
    },

    {
      icon: "📆",
      title: "Quarterly Plans",
      description:
        "Create quarterly plans aligned with annual goals.",
      onClick: () =>
        navigate("/planning/quarterly"),
    },

    {
      icon: "🎯",
      title: "Business Targets",
      description:
        "Define and track strategic business targets.",
      onClick: () =>
        navigate("/planning/targets"),
    },

    {
      icon: "📊",
      title: "Annual Dashboard",
      description:
        "View annual planning insights and forecasts.",
      onClick: () =>
        navigate("/planning/annual-dashboard"),
    },

    {
      icon: "📈",
      title: "Quarterly Dashboard",
      description:
        "Monitor quarterly performance and targets.",
      onClick: () =>
        navigate("/planning/quarterly-dashboard"),
    },

    {
      icon: "⚖️",
      title: "Forecast vs Target",
      description:
        "Compare forecasted demand against targets.",
      onClick: () =>
        navigate("/planning/forecast-vs-target"),
    },

    {
      icon: "🤖",
      title: "Planning Recommendations",
      description:
        "AI-generated strategic planning recommendations.",
      onClick: () =>
        navigate("/planning/recommendations"),
    },

  ];

  return (
    <Layout>

      <div className="p-8">

        <h1 className="text-3xl font-bold mb-2">
          Strategic Planning
        </h1>

        <p
          className={`mb-8 ${
            darkMode
              ? "text-gray-400"
              : "text-gray-500"
          }`}
        >
          Manage annual plans, quarterly plans,
          business targets, and planning analytics.
        </p>

        <div
          className="
            grid
            grid-cols-1
            md:grid-cols-2
            lg:grid-cols-3
            gap-6
          "
        >
          {cards.map((card) => (

            <div
              key={card.title}
              onClick={card.onClick}
              className={`
                cursor-pointer
                rounded-2xl
                shadow-lg
                p-6
                border
                hover:shadow-2xl
                hover:-translate-y-1
                transition-all
                duration-300

                ${
                  darkMode
                    ? "bg-gray-900 border-gray-800 text-white"
                    : "bg-white border-gray-200 text-gray-800"
                }
              `}
            >

              <div className="text-5xl mb-4">
                {card.icon}
              </div>

              <h2 className="text-xl font-semibold mb-2">
                {card.title}
              </h2>

              <p
                className={`text-sm ${
                  darkMode
                    ? "text-gray-400"
                    : "text-gray-500"
                }`}
              >
                {card.description}
              </p>

            </div>

          ))}
        </div>

      </div>

    </Layout>
  );
}

export default Strategic_Planning;