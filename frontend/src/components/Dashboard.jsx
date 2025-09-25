import { useState, useEffect } from "react";
import api from "../api"; // axios instance with baseURL + auth headers

export default function Dashboard() {
  const [tab, setTab] = useState("candidates");
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchData(tab);
  }, [tab]);

  async function fetchData(resource) {
    setLoading(true);
    setError("");
    try {
      const response = await api.get(`/business/${resource}`);
      setData(response.data);
    } catch (err) {
      console.error(`Failed to fetch ${resource}:`, err);
      setError("Could not load data.");
      setData([]);
    } finally {
      setLoading(false);
    }
  }

  const resources = [
  "candidates",
  "centres",
  "courses",
  "certificates",
  "cohorts",
  "users",
  "registrations",
  "issued-certificates", // use dash, not underscore
  ];


  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <h1 className="text-2xl font-bold mb-6">Accreditation Dashboard</h1>

      {/* Tab buttons */}
      <div className="flex flex-wrap gap-2 mb-6">
        {resources.map((resource) => (
          <button
            key={resource}
            onClick={() => setTab(resource)}
            className={`px-4 py-2 rounded ${
              tab === resource
                ? "bg-blue-600 text-white"
                : "bg-gray-200 text-gray-700 hover:bg-gray-300"
            }`}
          >
            {resource}
          </button>
        ))}
      </div>

      {/* Data section */}
      <div className="bg-white shadow rounded-lg p-4">
        <h2 className="text-xl font-semibold mb-4 capitalize">{tab}</h2>

        {loading ? (
          <p>Loading...</p>
        ) : error ? (
          <p className="text-red-500">{error}</p>
        ) : data.length === 0 ? (
          <p className="text-gray-500">No data found.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full border border-gray-200">
              <thead className="bg-gray-100">
                <tr>
                  {Object.keys(data[0]).map((key) => (
                    <th
                      key={key}
                      className="px-4 py-2 text-left text-sm font-medium text-gray-600 border-b"
                    >
                      {key}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {data.map((row, idx) => (
                  <tr key={idx} className="border-b hover:bg-gray-50">
                    {Object.keys(row).map((key) => (
                      <td
                        key={key}
                        className="px-4 py-2 text-sm text-gray-800"
                      >
                        {String(row[key])}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
