import "./Dashboard.css";
import KpiCards from "./KpiCards";
import RiskCharts from "./RiskCharts";
import Transactions from "./Transactions";

export default function Dashboard() {
  return (
    <div className="dashboard">
      <header className="dashboard-header fade-slide">
        <h1>VISA-NOVA Transaction Intelligence</h1>
        <p>AI-Powered Fraud & Risk Analytics</p>
      </header>

      <section className="section reveal">
        <KpiCards />
      </section>

      <section className="section reveal">
        <RiskCharts />
      </section>

      <section className="section reveal">
        <Transactions />
      </section>
    </div>
  );
}
