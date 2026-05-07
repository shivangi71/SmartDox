import { useState } from "react";

export default function BidderDashboard() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [step, setStep] = useState("upload");

  const uploadFile = async () => {
    if (!file) return alert("Upload file first");

    const formData = new FormData();
    formData.append("file", file);

    setStep("processing");

    const res = await fetch("http://127.0.0.1:8000/evaluate-bidder", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    setResult(data);
    setStep("result");
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">

      <h1 className="text-2xl font-bold mb-6">
        📄 Bidder Evaluation Portal
      </h1>

      {/* Upload */}
      {step === "upload" && (
        <div className="bg-white p-6 rounded-xl shadow max-w-xl">
          <input
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
            className="mb-4"
          />

          <button
            onClick={uploadFile}
            className="bg-blue-600 text-white px-4 py-2 rounded"
          >
            Upload & Evaluate
          </button>
        </div>
      )}

      {/* Processing */}
      {step === "processing" && (
        <div className="bg-white p-6 rounded-xl shadow">
          <h2 className="font-bold">🔄 AI Processing Document</h2>
          <p>Extracting and evaluating criteria...</p>
        </div>
      )}

      {/* RESULT (FULL POWER RESTORED 🔥) */}
      {step === "result" && result && (
        <div className="grid md:grid-cols-2 gap-6 mt-6">

          {/* LEFT - SUMMARY */}
          <div className="bg-white p-5 rounded-xl shadow">
            <h2 className="text-xl font-bold mb-3">Final Result</h2>

            <div className={`p-3 text-white text-center rounded ${
              result.final_status === "Eligible" ? "bg-green-500" : "bg-red-500"
            }`}>
              {result.final_status}
            </div>

            <p className="mt-3 font-semibold">Evaluation Breakdown:</p>

            <div className="mt-2 space-y-2">
              {Object.entries(result.evaluation).map(([key, value]) => (
                <div key={key} className="flex justify-between border-b pb-1">
                  <span className="capitalize">{key}</span>
                  <span className={value === "PASS" ? "text-green-600 font-bold" : "text-red-600 font-bold"}>
                    {value}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* RIGHT - DETAILED EXPLANATION (IMPORTANT RESTORED 🔥) */}
          <div className="bg-white p-5 rounded-xl shadow">
            <h2 className="text-xl font-bold mb-3">AI Detailed Explanation</h2>

            <div className="space-y-4 max-h-[500px] overflow-auto">
              {Object.entries(result.explanation).map(([key, val]) => (
                <div key={key} className="border p-3 rounded-lg">
                  <h3 className="font-bold uppercase">{key}</h3>

                  <p><b>Status:</b> {val.status}</p>
                  <p><b>Required:</b> {val.required}</p>
                  <p><b>Found:</b> {val.found}</p>
                  <p className="text-sm text-gray-600">{val.reason}</p>
                </div>
              ))}
            </div>
          </div>

        </div>
      )}

    </div>
  );
}