import { useState } from "react";
import axios from "axios";

function App() {
  const [websiteName, setWebsiteName] = useState("");
  const [url, setUrl] = useState("");

  const [result, setResult] = useState(null);
  const [allResults, setAllResults] = useState([]);

  const [loading, setLoading] = useState(false);

  const enrichCompany = async () => {
    try {
      setLoading(true);

      const response = await axios.post(
        "http://127.0.0.1:8000/enrich",
        {
          website_name: websiteName,
          url: url,
        }
      );

      setResult(response.data);
    } catch (error) {
      console.error(error);
      alert("Error enriching company");
    } finally {
      setLoading(false);
    }
  };

  const fetchResults = async () => {
    try {
      const response = await axios.get(
        "http://127.0.0.1:8000/results"
      );

      setAllResults(response.data);
    } catch (error) {
      console.error(error);
      alert("Error fetching results");
    }
  };

  return (
    <div style={{ padding: "30px" }}>
      <h1>Prospect Research Agent</h1>

      <hr />

      <h2>Enrich Company</h2>

      <input
        type="text"
        placeholder="Website Name"
        value={websiteName}
        onChange={(e) =>
          setWebsiteName(e.target.value)
        }
        style={{
          width: "300px",
          marginBottom: "10px",
          display: "block",
        }}
      />

      <input
        type="text"
        placeholder="Company URL"
        value={url}
        onChange={(e) =>
          setUrl(e.target.value)
        }
        style={{
          width: "300px",
          marginBottom: "10px",
          display: "block",
        }}
      />

      <button onClick={enrichCompany}>
        {loading ? "Researching..." : "Enrich"}
      </button>

      {result && (
        <div
          style={{
            marginTop: "20px",
            border: "1px solid gray",
            padding: "15px",
          }}
        >
          <h3>{result.company_name}</h3>

          <p>
            <strong>Address:</strong>{" "}
            {result.address}
          </p>

          <p>
            <strong>Phone:</strong>{" "}
            {result.mobile_number}
          </p>

          <p>
            <strong>Emails:</strong>{" "}
            {result.mail?.join(", ")}
          </p>

          <p>
            <strong>Core Service:</strong>{" "}
            {result.core_service}
          </p>

          <p>
            <strong>Target Customer:</strong>{" "}
            {result.target_customer}
          </p>

          <p>
            <strong>Pain Point:</strong>{" "}
            {result.probable_pain_point}
          </p>

          <p>
            <strong>Outreach:</strong>{" "}
            {result.outreach_opener}
          </p>
        </div>
      )}

      <hr />

      <h2>Results</h2>

      <button onClick={fetchResults}>
        Show All Results
      </button>

      {allResults.length > 0 && (
        <table
          border="1"
          cellPadding="10"
          style={{
            marginTop: "20px",
            width: "100%",
          }}
        >
          <thead>
            <tr>
              <th>Company</th>
              <th>Service</th>
              <th>Target Customer</th>
            </tr>
          </thead>

          <tbody>
            {allResults.map((item, index) => (
              <tr key={index}>
                <td>{item.company_name}</td>

                <td>{item.core_service}</td>

                <td>
                  {item.target_customer}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default App;