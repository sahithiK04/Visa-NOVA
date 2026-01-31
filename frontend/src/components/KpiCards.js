import React, { useEffect, useState } from "react";
import "./KpiCards.css";

function KpiCards() {
  const [metrics, setMetrics] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/analytics/summary")
      .then((res) => res.json())
      .then((data) => setMetrics(data.metrics))
      .catch((err) => console.error(err));
  }, []);

  if (!metrics) return <p>Loading metrics...</p>;

  return (
    <div className="kpi-grid">
      <div className="kpi-card">
        <h3>Precision</h3>
        <p>{metrics.precision}</p>
      </div>

      <div className="kpi-card">
        <h3>Recall</h3>
        <p>{metrics.recall}</p>
      </div>
    </div>
  );
}

export default KpiCards;
