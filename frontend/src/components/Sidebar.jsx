export default function Sidebar({ setTab }) {
  return (
    <div className="w-64 h-screen bg-blue-900 text-white p-5">

      <h1 className="text-xl font-bold mb-6">SmartDOX</h1>

      <button onClick={() => setTab("dashboard")} className="block w-full text-left py-2 hover:bg-blue-700 px-2 rounded">
        📊 Dashboard
      </button>

      <button onClick={() => setTab("bidders")} className="block w-full text-left py-2 hover:bg-blue-700 px-2 rounded">
        📄 Bidders
      </button>

      <button onClick={() => setTab("reports")} className="block w-full text-left py-2 hover:bg-blue-700 px-2 rounded">
        📑 Reports
      </button>

      <button onClick={() => setTab("audit")} className="block w-full text-left py-2 hover:bg-blue-700 px-2 rounded">
        🔍 Audit Logs
      </button>

    </div>
  );
}