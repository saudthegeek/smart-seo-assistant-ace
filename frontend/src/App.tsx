import { useState } from 'react'

import './App.css'

function App() {
  const [keyword, setKeyword] = useState("");
  const [brief, setBrief] = useState("");

  const generateBrief = async () => {
    const response = await axios.post("http://localhost:8000/generate-brief", { keyword });
    setBrief(response.data.brief);
  };

  return (
    <div className="p-4 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Smart SEO Assistant</h1>
      <input
        type="text"
        value={keyword}
        onChange={(e) => setKeyword(e.target.value)}
        placeholder="Enter a keyword..."
        className="border p-2 w-full mb-4"
      />
      <button onClick={generateBrief} className="bg-blue-500 text-white px-4 py-2 rounded">
        Generate Brief
      </button>
      <div className="mt-6">
        <h2 className="text-lg font-semibold">Generated Brief:</h2>
        <pre className="bg-gray-100 p-4 mt-2 whitespace-pre-wrap">{brief}</pre>
      </div>
    </div>
  );
}

export default App;
