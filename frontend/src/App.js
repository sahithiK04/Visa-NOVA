import "./App.css";
import Transactions from "./components/Transactions";
import Anomalies from "./components/Anomalies";
import Analytics from "./components/Analytics";
import KpiCards from "./components/KpiCards";
import RiskCharts from "./components/RiskCharts";

function App() {
  return (
    <div className="dashboard">
      <h1>VISA-NOVA Transaction Intelligence</h1>

      <KpiCards />
      <RiskCharts />

      <hr />

      <Anomalies />
      <hr />

      <Transactions />
    </div>
  );
}

export default App;
