import React, { useEffect, useState } from "react";

function Analytics() {
  const [summary, setSummary] = useState(null);
  const [distribution, setDistribution] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/analytics/summary")
      .then((res) => res.json())
      .then((data) => setSummary(data));

    fetch("http://127.0.0.1:8000/analytics/risk-distribution")
      .then((res) => res.json())
      .then((data) => setDistribution(data));
  }, []);

  if (!summary) return <p>Loading analytics...</p>;

  const cm = summary.confusion_matrix;
  const metrics = summary.metrics;

  return (
    <div>
      <h2>Model Analytics</h2>

      <h3>Metrics</h3>
      <ul>
        <li>Precision: <b>{metrics.precision}</b></li>
        <li>Recall: <b>{metrics.recall}</b></li>
      </ul>

      <h3>Confusion Matrix</h3>
      <ul>
        <li>True Positive: {cm.true_positive}</li>
        <li>False Positive: {cm.false_positive}</li>
        <li>False Negative: {cm.false_negative}</li>
        <li>True Negative: {cm.true_negative}</li>
      </ul>

      <h3>Risk Distribution</h3>
      <table border="1" cellPadding="8">
        <thead>
          <tr>
            <th>Risk Level</th>
            <th>Total Transactions</th>
            <th>Fraud Transactions</th>
          </tr>
        </thead>
        <tbody>
          {distribution.map((row) => (
            <tr key={row.risk_level}>
              <td>{row.risk_level}</td>
              <td>{row.total_transactions}</td>
              <td>{row.fraud_transactions}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Analytics;
