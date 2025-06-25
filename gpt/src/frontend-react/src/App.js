// file: frontend-react/src/App.js
import React, { useState, useEffect } from 'react';
import './App.css'; // This line now correctly imports the CSS file

// Define the API endpoints.
const GO_API_URL = 'http://localhost:8080';
const PYTHON_API_URL = 'http://localhost:5000';

function App() {
  // State to hold the counts from the database
  const [goCount, setGoCount] = useState(0);
  const [pythonCount, setPythonCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Function to fetch the latest counts from the Go API
  const fetchCounts = async () => {
    try {
      const response = await fetch(`${GO_API_URL}/api/counts`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setGoCount(data.go_count);
      setPythonCount(data.python_count);
    } catch (e) {
      setError(`Failed to fetch counts: ${e.message}`);
      console.error("Fetch counts error:", e);
    }
  };

  // useEffect hook runs on component mount (page load/refresh)
  useEffect(() => {
    const incrementAndFetch = async () => {
      try {
        console.log("Attempting to increment Go count on page load...");
        // 1. Increment the Go counter
        await fetch(`${GO_API_URL}/api/go/increment`, { method: 'POST' });
        console.log("Go count incremented. Fetching new counts...");
        // 2. Fetch the updated counts
        await fetchCounts();
      } catch (e) {
        setError(`Initial load error: ${e.message}`);
        console.error("Initial load error:", e);
      } finally {
        setLoading(false);
      }
    };

    incrementAndFetch();
  }, []); // The empty array ensures this runs only once on mount

  // Handler for the button click
  const handlePythonClick = async () => {
    try {
      // 1. Increment the Python counter
      await fetch(`${PYTHON_API_URL}/api/python/increment`, { method: 'POST' });
      // 2. Fetch the updated counts to refresh the UI
      await fetchCounts();
    } catch (e) {
        setError(`Python API call error: ${e.message}`);
        console.error("Python API call error:", e);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Welcome to the 3-Tier App!</h1>
        <p>This page refresh was served by the Go API.</p>
        <button onClick={handlePythonClick}>
          Click Me to Call the Python API
        </button>
        <div className="counts">
          <h2>Request Counts</h2>
          {loading ? (
            <p>Initializing and fetching counts...</p>
          ) : error ? (
            <p className="error">{error}</p>
          ) : (
            <>
              <p>Go API Requests: <span>{goCount}</span></p>
              <p>Python API Requests: <span>{pythonCount}</span></p>
            </>
          )}
        </div>
      </header>
    </div>
  );
}

export default App;