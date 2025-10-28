import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import TeamDashboard from './pages/TeamDashboard';
import AthleteDetail from './pages/AthleteDetail';
import DataUpload from './pages/DataUpload';
import AthleteManagement from './pages/AthleteManagement';
import ConnectionTest from './pages/ConnectionTest';

function App() {
  return (
    <Router>
      <div className="App">
        <nav>
          <div className="container">
            <h1>Sports Medicine - Injury Prevention System</h1>
            <ul>
              <li><Link to="/">Team Dashboard</Link></li>
              <li><Link to="/athletes">Manage Athletes</Link></li>
              <li><Link to="/upload">Upload Data</Link></li>
              <li><Link to="/test">Connection Test</Link></li>
            </ul>
          </div>
        </nav>

        <div className="container">
          <Routes>
            <Route path="/" element={<TeamDashboard />} />
            <Route path="/athletes" element={<AthleteManagement />} />
            <Route path="/athlete/:id" element={<AthleteDetail />} />
            <Route path="/upload" element={<DataUpload />} />
            <Route path="/test" element={<ConnectionTest />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
