import { useState } from "react";
import "./index.css";

import { getHealthData, uploadCSV } from "./services/api";

import ScoreCard from "./components/ScoreCard";
import TrendCard from "./components/TrendCard";
import SummaryCard from "./components/SummaryCard";

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const loadHealthData = async () => {
    try {
      const res = await getHealthData();
      setData(res);
    } catch (err) {
      console.error(err);
      alert("Unable to analyze the uploaded CSV.");
    }

    setLoading(false);
  };

  const handleUpload = async (event) => {
    const file = event.target.files[0];

    if (!file) return;

    try {
      setLoading(true);

      await uploadCSV(file);

      await loadHealthData();

    } catch (err) {
      console.error(err);
      alert("Upload failed.");
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="loader"></div>

        <h1>Analyzing Health Data...</h1>

        <p>IBM Granite AI is generating personalized wellness insights.</p>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="landing">

        <div className="hero">

          <h1>🧠 VitalMind AI</h1>

          <h2>AI-Powered Wearable Health Analytics</h2>

          <p>
            Upload your smartwatch health CSV to receive personalized wellness
            insights powered by IBM Granite.
          </p>

        </div>

        <label className="upload-card">

          <div className="upload-icon">📂</div>

          <h2>Upload Health CSV</h2>

          <p>
            Apple Watch • Fitbit • Garmin • Samsung Health
          </p>

          <input
            type="file"
            accept=".csv"
            onChange={handleUpload}
            hidden
          />

          <div className="upload-btn">
            Browse CSV
          </div>

        </label>

        <div className="footer">

          Powered by IBM watsonx.ai • Granite • React • FastAPI

        </div>

      </div>
    );
  }

  const summary = data.health_summary;

  return (
    <div className="container">

      <header className="dashboard-header">

        <div>

          <h1>🧠 VitalMind AI</h1>

          <p>AI Powered Wellness Dashboard</p>

        </div>

        <label className="small-upload">

          Upload CSV

          <input
            type="file"
            accept=".csv"
            hidden
            onChange={handleUpload}
          />

        </label>

      </header>

      <section className="score-grid">

        <ScoreCard
          title="Wellness Score"
          value={summary.wellness_score}
        />

        <ScoreCard
          title="Recovery Score"
          value={summary.recovery_score}
        />

      </section>

      <section className="score-grid">

        <ScoreCard
          title="😴 Sleep"
          value={`${summary.averages.Sleep_Hours} hrs`}
        />

        <ScoreCard
          title="❤️ HRV"
          value={`${summary.averages.HRV} ms`}
        />

        <ScoreCard
          title="👣 Steps"
          value={summary.averages.Steps}
        />

        <ScoreCard
          title="💓 Resting HR"
          value={summary.averages.Resting_Heart_Rate}
        />

      </section>

      <section className="score-grid">

        <TrendCard
          title="Sleep Trend"
          value={summary.trends.Sleep_Hours}
        />

        <TrendCard
          title="Heart Rate Trend"
          value={summary.trends.Resting_Heart_Rate}
        />

      </section>

      <SummaryCard text={data.ai_summary} />

      <footer className="dashboard-footer">

        VitalMind AI • IBM watsonx.ai • Granite • FastAPI • React

      </footer>

    </div>
  );
}

export default App;