import React from "react";

function ScoreCard({ title, value }) {

  const numericValue = parseFloat(value);

  const isScore =
    title === "Wellness Score" ||
    title === "Recovery Score";

  let color = "#60a5fa";
  let status = "";

  if (isScore) {

    if (numericValue >= 80) {
      color = "#22c55e";
      status = "Excellent";
    } else if (numericValue >= 60) {
      color = "#facc15";
      status = "Good";
    } else if (numericValue >= 40) {
      color = "#fb923c";
      status = "Fair";
    } else {
      color = "#ef4444";
      status = "Poor";
    }

  }

  const radius = 55;
  const circumference = 2 * Math.PI * radius;

  const progress = isScore
    ? circumference - (numericValue / 100) * circumference
    : circumference;

  return (
    <div className="card">

      {isScore ? (

        <div
          style={{
            display: "flex",
            justifyContent: "center",
            marginBottom: "20px",
          }}
        >

          <svg width="140" height="140">

            <circle
              cx="70"
              cy="70"
              r={radius}
              stroke="rgba(255,255,255,.15)"
              strokeWidth="12"
              fill="none"
            />

            <circle
              cx="70"
              cy="70"
              r={radius}
              stroke={color}
              strokeWidth="12"
              fill="none"
              strokeLinecap="round"
              strokeDasharray={circumference}
              strokeDashoffset={progress}
              transform="rotate(-90 70 70)"
            />

            <text
              x="70"
              y="78"
              textAnchor="middle"
              fill="white"
              fontSize="28"
              fontWeight="bold"
            >
              {numericValue}
            </text>

          </svg>

        </div>

      ) : (

        <h1
          style={{
            fontSize: "42px",
            marginBottom: "15px",
          }}
        >
          {value}
        </h1>

      )}

      <h3>{title}</h3>

      {isScore && (

        <p
          style={{
            color,
            fontWeight: "bold",
            marginTop: "12px",
            fontSize: "18px",
          }}
        >
          {status}
        </p>

      )}

    </div>
  );

}

export default ScoreCard;