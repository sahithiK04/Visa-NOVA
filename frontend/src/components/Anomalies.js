import React, { useEffect, useState } from "react";

function Anomalies() {
  const [anomalies, setAnomalies] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/transactions/anomalies?limit=10&offset=0")
      .then((res) => res.json())
      .then((data) => setAnomalies(data.data));
  }, []);

  return (
    <div>
      <h2>High-Risk Transactions (ML)</h2>
      <table border="1" cellPadding="8">
        <thead>
          <tr>
            <th>ID</th>
            <th>Amount</th>
            <th>Anomaly Score</th>
            <th>Risk</th>
          </tr>
        </thead>
        <tbody>
          {anomalies.map((tx) => (
            <tr key={tx.id}>
              <td>{tx.id}</td>
              <td>{tx.amount}</td>
              <td>{tx.anomaly_score?.toFixed(3)}</td>
              <td>{tx.risk_level}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Anomalies;

