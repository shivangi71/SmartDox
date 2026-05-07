import { useState } from "react";
import BidderDashboard from "./pages/BidderDashboard";
import AdminDashboard from "./pages/AdminDashboard";

export default function App() {
  const [role, setRole] = useState(null);

  if (role === "admin") return <AdminDashboard />;
  if (role === "bidder") return <BidderDashboard />;

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-slate-100 via-blue-50 to-slate-200">

      {/* TOP NAVBAR */}
      <header className="bg-blue-900 text-white px-8 py-4 shadow-lg flex justify-between items-center">
        <div>
          <h1 className="text-xl font-bold">SmartDOX AI System</h1>
          <p className="text-xs text-blue-200">
            Government Tender Evaluation Platform (CRPF Prototype)
          </p>
        </div>

        <div className="text-xs bg-blue-700 px-3 py-1 rounded-full">
          Secure AI Evaluation Engine
        </div>
      </header>

      {/* HERO SECTION */}
      <main className="flex-1 flex flex-col items-center justify-center p-6">

        <div className="text-center mb-10">
          <h2 className="text-4xl font-extrabold text-gray-800">
            SmartDOX Procurement Intelligence
          </h2>
          <p className="text-gray-600 mt-2 max-w-2xl">
            AI-powered tender evaluation system that automates eligibility checks,
            document verification, and compliance analysis for government procurement.
          </p>
        </div>

        {/* FEATURE CARDS */}
        <div className="grid md:grid-cols-3 gap-6 max-w-5xl w-full">

          <div className="bg-white p-6 rounded-2xl shadow-md border hover:shadow-xl transition">
            <h3 className="font-bold text-blue-700">📄 Document Intelligence</h3>
            <p className="text-sm text-gray-600 mt-2">
              Extracts structured data from PDFs, scans, and certificates using AI + OCR.
            </p>
          </div>

          <div className="bg-white p-6 rounded-2xl shadow-md border hover:shadow-xl transition">
            <h3 className="font-bold text-green-700">🧠 AI Evaluation Engine</h3>
            <p className="text-sm text-gray-600 mt-2">
              Automatically evaluates turnover, GST, ISO, and project compliance.
            </p>
          </div>

          <div className="bg-white p-6 rounded-2xl shadow-md border hover:shadow-xl transition">
            <h3 className="font-bold text-purple-700">🔍 Audit & Transparency</h3>
            <p className="text-sm text-gray-600 mt-2">
              Fully explainable decisions with traceable evaluation reports.
            </p>
          </div>

        </div>

        {/* ROLE SELECTION SECTION */}
        <div className="mt-12 w-full max-w-4xl">

          <h3 className="text-center text-xl font-bold text-gray-700 mb-6">
            Select Your Access Role
          </h3>

          <div className="grid md:grid-cols-2 gap-6">

            {/* ADMIN CARD */}
            <div
              onClick={() => setRole("admin")}
              className="cursor-pointer bg-gradient-to-r from-blue-600 to-blue-800 text-white p-8 rounded-2xl shadow-lg hover:scale-105 transition"
            >
              <div className="text-4xl">👮</div>
              <h4 className="text-xl font-bold mt-3">CRPF Officer Portal</h4>
              <p className="text-sm text-blue-100 mt-2">
                Evaluate bidders, view AI reports, approve or reject tenders.
              </p>

              <div className="mt-4 text-xs bg-blue-500 inline-block px-3 py-1 rounded-full">
                Admin Access
              </div>
            </div>

            {/* BIDDER CARD */}
            <div
              onClick={() => setRole("bidder")}
              className="cursor-pointer bg-gradient-to-r from-green-500 to-green-700 text-white p-8 rounded-2xl shadow-lg hover:scale-105 transition"
            >
              <div className="text-4xl">📄</div>
              <h4 className="text-xl font-bold mt-3">Bidder Submission Portal</h4>
              <p className="text-sm text-green-100 mt-2">
                Upload documents, check eligibility, and track evaluation status.
              </p>

              <div className="mt-4 text-xs bg-green-400 inline-block px-3 py-1 rounded-full">
                Applicant Access
              </div>
            </div>

          </div>
        </div>

      </main>

      {/* FOOTER */}
      <footer className="text-center text-xs text-gray-500 py-4">
        SmartDOX © 2026 | AI-Powered Government Procurement System | Prototype
      </footer>

    </div>
  );
}