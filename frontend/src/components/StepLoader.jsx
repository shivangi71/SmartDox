export default function StepLoader() {
  return (
    <div className="bg-white p-6 rounded-xl shadow">
      <h2 className="font-bold mb-3">AI Processing Tender...</h2>

      <ul className="space-y-2 text-sm">
        <li>✔ Extracting document text</li>
        <li>✔ Identifying eligibility criteria</li>
        <li>✔ Validating GST / ISO / Turnover</li>
        <li>🔄 Running AI evaluation engine</li>
      </ul>
    </div>
  );
}