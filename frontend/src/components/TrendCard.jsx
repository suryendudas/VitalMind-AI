function TrendCard({ title, value }) {

  let icon = "➖";
  let color = "#94a3b8";
  let message = "Stable";

  if (value === "increasing") {

    icon = "📈";

    if (title.includes("Heart")) {
      color = "#ef4444";
      message = "Needs Attention";
    } else {
      color = "#22c55e";
      message = "Improving";
    }

  }

  if (value === "decreasing") {

    icon = "📉";

    if (title.includes("Sleep")) {
      color = "#ef4444";
      message = "Needs Attention";
    } else {
      color = "#22c55e";
      message = "Improving";
    }

  }

  if (value === "stable") {

    icon = "➖";
    color = "#facc15";
    message = "Stable";

  }

  return (

    <div className="card">

      <div
        style={{
          fontSize: "65px",
          marginBottom: "15px",
        }}
      >
        {icon}
      </div>

      <h3>{title}</h3>

      <h2
        style={{
          color,
          marginTop: "15px",
        }}
      >
        {value.toUpperCase()}
      </h2>

      <p
        style={{
          marginTop: "15px",
          opacity: ".9",
          fontWeight: "bold",
          color,
        }}
      >
        {message}
      </p>

    </div>

  );

}

export default TrendCard;