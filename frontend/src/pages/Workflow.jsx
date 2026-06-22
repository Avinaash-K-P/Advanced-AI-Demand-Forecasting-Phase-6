import Layout from "../components/Layout";
import { useNavigate } from "react-router-dom";

function Workflow() {

  const navigate = useNavigate();

  const darkMode =
    localStorage.getItem("theme") === "dark";

  const cards = [
    {
      icon: "⚙️",
      title: "Create Workflow",
      description:
        "Create automation workflows for approval and business processes.",
      onClick: () =>
        navigate("/workflow/create"),
    },
    {
      icon: "📋",
      title: "View Workflows",
      description:
        "View all configured workflows and their settings.",
      onClick: () =>
        navigate("/workflow/view"),
    },
    {
      icon: "➕",
      title: "Create Workflow Step",
      description:
        "Add workflow steps and approval stages.",
      onClick: () =>
        navigate("/workflow/steps"),
    },
    {
      icon: "▶",
      title: "Execute Workflow",
      description:
        "Trigger and execute workflow automation.",
      onClick: () =>
        navigate("/workflow/execute"),
    },
    {
      icon: "📊",
      title: "Execution History",
      description:
        "Review workflow execution history and status.",
      onClick: () =>
        navigate("/workflow/executions"),
    },
    {
      icon: "📝",
      title: "Workflow Logs",
      description:
        "View workflow logs and execution events.",
      onClick: () =>
        navigate("/workflow/logs"),
    },
  ];

  return (
    <Layout>
      <div className="p-8">

        <h1 className="text-3xl font-bold mb-2">
          Workflow Automation
        </h1>

        <p
          className={`mb-8 ${
            darkMode
              ? "text-gray-400"
              : "text-gray-500"
          }`}
        >
          Manage workflow automation, approvals,
          execution history, and process logs.
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
                transition-all
                duration-300
                hover:shadow-2xl
                hover:-translate-y-1
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

export default Workflow;