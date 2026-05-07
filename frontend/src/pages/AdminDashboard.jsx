import { useState } from "react";
import Sidebar from "../components/Sidebar";

export default function AdminDashboard() {
  const [tab, setTab] = useState("dashboard");

  return (
    <div className="flex">

      <Sidebar setTab={setTab} />

      <div className="flex-1 p-6 bg-gray-100 min-h-screen">

        <h1 className="text-2xl font-bold mb-6">
          👮 CRPF Admin Panel
        </h1>

        {tab === "dashboard" && (
          <div className="bg-white p-6 rounded-xl shadow">
            <h2 className="font-bold">System Overview</h2>
            <p>Total Bidders: 120</p>
            <p>Eligible: 80</p>
            <p>Under Review: 25</p>
            <p>Rejected: 15</p>
          </div>
        )}

        {tab === "bidders" && (
          <div className="bg-white p-6 rounded-xl shadow">
            <h2 className="font-bold mb-3">Bidder List</h2>
            <ul>
              <li>Bidder A - Eligible</li>
              <li>Bidder B - Under Review</li>
              <li>Bidder C - Rejected</li>
            </ul>
          </div>
        )}

      </div>
    </div>
  );
}