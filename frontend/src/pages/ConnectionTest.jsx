import React, { useState, useEffect } from 'react';
import axios from 'axios';

function ConnectionTest() {
  const [tests, setTests] = useState({
    backend_localhost: { status: 'testing', message: '' },
    backend_127: { status: 'testing', message: '' },
    api_health: { status: 'testing', message: '' },
    api_athletes: { status: 'testing', message: '' },
  });

  useEffect(() => {
    runTests();
  }, []);

  const runTests = async () => {
    // Test 1: Backend on localhost
    try {
      const response = await axios.get('http://localhost:8000', { timeout: 3000 });
      setTests(prev => ({
        ...prev,
        backend_localhost: {
          status: 'success',
          message: `Connected! Response: ${response.data.message || 'OK'}`
        }
      }));
    } catch (error) {
      setTests(prev => ({
        ...prev,
        backend_localhost: {
          status: 'error',
          message: error.message
        }
      }));
    }

    // Test 2: Backend on 127.0.0.1
    try {
      const response = await axios.get('http://127.0.0.1:8000', { timeout: 3000 });
      setTests(prev => ({
        ...prev,
        backend_127: {
          status: 'success',
          message: `Connected! Response: ${response.data.message || 'OK'}`
        }
      }));
    } catch (error) {
      setTests(prev => ({
        ...prev,
        backend_127: {
          status: 'error',
          message: error.message
        }
      }));
    }

    // Test 3: Health endpoint
    try {
      const response = await axios.get('http://127.0.0.1:8000/health', { timeout: 3000 });
      setTests(prev => ({
        ...prev,
        api_health: {
          status: 'success',
          message: `Health: ${response.data.status || 'OK'}`
        }
      }));
    } catch (error) {
      setTests(prev => ({
        ...prev,
        api_health: {
          status: 'error',
          message: error.message
        }
      }));
    }

    // Test 4: Athletes endpoint
    try {
      const response = await axios.get('http://127.0.0.1:8000/athletes/', { timeout: 3000 });
      setTests(prev => ({
        ...prev,
        api_athletes: {
          status: 'success',
          message: `Athletes endpoint working! Found ${response.data.length} athletes`
        }
      }));
    } catch (error) {
      setTests(prev => ({
        ...prev,
        api_athletes: {
          status: 'error',
          message: error.message
        }
      }));
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'success': return '#27ae60';
      case 'error': return '#e74c3c';
      case 'testing': return '#f39c12';
      default: return '#95a5a6';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'success': return '✓';
      case 'error': return '✗';
      case 'testing': return '⟳';
      default: return '?';
    }
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Connection Diagnostic Test</h2>
      <p>This page tests the connection between frontend and backend.</p>

      <div style={{ marginTop: '2rem' }}>
        {Object.entries(tests).map(([key, test]) => (
          <div
            key={key}
            style={{
              padding: '1rem',
              marginBottom: '1rem',
              border: `2px solid ${getStatusColor(test.status)}`,
              borderRadius: '8px',
              backgroundColor: test.status === 'success' ? '#d4edda' : test.status === 'error' ? '#f8d7da' : '#fff3cd'
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <span style={{ fontSize: '1.5rem', color: getStatusColor(test.status) }}>
                {getStatusIcon(test.status)}
              </span>
              <div style={{ flex: 1 }}>
                <strong>{key.replace(/_/g, ' ').toUpperCase()}</strong>
                <div style={{ marginTop: '0.5rem', color: '#666' }}>
                  {test.message || 'Testing...'}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div style={{ marginTop: '2rem', padding: '1rem', backgroundColor: '#e9ecef', borderRadius: '8px' }}>
        <h3>What These Tests Mean:</h3>
        <ul>
          <li><strong>Backend localhost</strong>: Tests if backend is accessible via http://localhost:8000</li>
          <li><strong>Backend 127.0.0.1</strong>: Tests if backend is accessible via http://127.0.0.1:8000</li>
          <li><strong>API health</strong>: Tests the /health endpoint</li>
          <li><strong>API athletes</strong>: Tests the /athletes/ endpoint (used by dashboard)</li>
        </ul>
      </div>

      <div style={{ marginTop: '2rem' }}>
        <h3>Troubleshooting:</h3>
        <div style={{ backgroundColor: '#fff', padding: '1rem', borderRadius: '8px', marginTop: '1rem' }}>
          {tests.backend_127.status === 'error' && tests.backend_localhost.status === 'error' ? (
            <div style={{ color: '#e74c3c' }}>
              <strong>⚠️ Backend is NOT running!</strong>
              <p>Solution:</p>
              <ol>
                <li>Check the Backend terminal window</li>
                <li>You should see: "Uvicorn running on http://127.0.0.1:8000"</li>
                <li>If not, close all windows and run START_APP.bat again</li>
              </ol>
            </div>
          ) : tests.backend_127.status === 'success' ? (
            <div style={{ color: '#27ae60' }}>
              <strong>✓ Backend is running!</strong>
              <p>The connection is working properly.</p>
            </div>
          ) : (
            <div style={{ color: '#f39c12' }}>
              <strong>⚠️ Mixed results</strong>
              <p>Try restarting both servers with START_APP.bat</p>
            </div>
          )}
        </div>
      </div>

      <button
        onClick={runTests}
        style={{
          marginTop: '2rem',
          padding: '1rem 2rem',
          backgroundColor: '#3498db',
          color: 'white',
          border: 'none',
          borderRadius: '6px',
          cursor: 'pointer',
          fontSize: '1rem'
        }}
      >
        Re-run Tests
      </button>
    </div>
  );
}

export default ConnectionTest;
