import React, { useEffect, useState } from "react";

const LIMIT = 10;

function Transactions() {
  const [transactions, setTransactions] = useState([]);
  const [offset, setOffset] = useState(0);
  const [selectedRisk, setSelectedRisk] = useState("ALL");

  useEffect(() => {
    fetch(
      `http://127.0.0.1:8000/transactions?limit=${LIMIT}&offset=${offset}`
    )
      .then((res) => res.json())
      .then((data) => setTransactions(data.data))
      .catch((err) => console.error(err));
  }, [offset]);

  const riskColor = (risk) => {
    if (risk === "HIGH") return "#f8d7da";    // red
    if (risk === "MEDIUM") return "#fff3cd"; // yellow
    return "#d4edda";                         // green
  };

  return (
    <div>
      <h2>All Transactions</h2>

      <label>Filter by Risk: </label>
      <select
        value={selectedRisk}
        onChange={(e) => setSelectedRisk(e.target.value)}
      >
        <option value="ALL">ALL</option>
        <option value="LOW">LOW</option>
        <option value="MEDIUM">MEDIUM</option>
        <option value="HIGH">HIGH</option>
      </select>

      <br /><br />

      <table border="1" cellPadding="8" width="100%">
        <thead>
          <tr>
            <th>ID</th>
            <th>Amount</th>
            <th>Actual Fraud</th>
            <th>Risk Level</th>
          </tr>
        </thead>

        <tbody>
          {transactions
            .filter(
              (tx) =>
                selectedRisk === "ALL" ||
                tx.risk_level === selectedRisk
            )
            .map((tx) => (
              <tr
                key={tx.id}
                style={{ backgroundColor: riskColor(tx.risk_level) }}
              >
                <td>{tx.id}</td>
                <td>{tx.amount}</td>
                <td>{tx.actual_fraud ? "Yes" : "No"}</td>
                <td>{tx.risk_level}</td>
              </tr>
            ))}
        </tbody>
      </table>

      <br />

      <button onClick={() => setOffset(Math.max(0, offset - LIMIT))}>
        Previous
      </button>
      &nbsp;
      <button onClick={() => setOffset(offset + LIMIT)}>
        Next
      </button>
    </div>
  );
}

export default Transactions;
