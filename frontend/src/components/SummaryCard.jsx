function SummaryCard({ text }) {

  const formatText = () => {

    if (!text) return [];

    const lines = text.split("\n").filter(line => line.trim() !== "");

    return lines.map((line, index) => {

      let icon = "";

      if (line.startsWith("Overall Wellness"))
        icon = "🟢";

      else if (line.startsWith("Recovery"))
        icon = "💪";

      else if (line.startsWith("Sleep"))
        icon = "😴";

      else if (line.startsWith("Heart Rate"))
        icon = "❤️";

      else if (line.startsWith("Recommendations"))
        icon = "💡";

      if (icon) {

        return (
          <div key={index} className="summary-section">

            <h3>
              {icon} {line}
            </h3>

          </div>
        );

      }

      if (line.startsWith("-")) {

        return (

          <p key={index} className="summary-bullet">

            ✔ {line.substring(1).trim()}

          </p>

        );

      }

      return (

        <p key={index} className="summary-paragraph">

          {line}

        </p>

      );

    });

  };

  return (

    <div className="summary-card">

      <h2>🤖 AI Wellness Coach</h2>

      {formatText()}

    </div>

  );

}

export default SummaryCard;