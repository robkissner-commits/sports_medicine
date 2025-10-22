import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getTeamOverview, calculateAllRisks } from '../services/api';

function TeamDashboard() {
  const [overview, setOverview] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [riskFilter, setRiskFilter] = useState(null);
  const [calculating, setCalculating] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    loadOverview();
  }, [riskFilter]);

  const loadOverview = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await getTeamOverview(null, riskFilter);
      setOverview(response.data);
    } catch (err) {
      setError('Failed to load team overview: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCalculateRisks = async () => {
    try {
      setCalculating(true);
      await calculateAllRisks();
      alert('Risk calculations completed successfully!');
      loadOverview();
    } catch (err) {
      alert('Failed to calculate risks: ' + err.message);
    } finally {
      setCalculating(false);
    }
  };

  const getRiskClass = (level) => {
    switch (level) {
      case 'high': return 'risk-high';
      case 'medium': return 'risk-medium';
      case 'low': return 'risk-low';
      default: return '';
    }
  };

  if (loading) {
    return <div className="loading">Loading team overview...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  if (!overview) {
    return <div className="loading">No data available</div>;
  }

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h2>Team Overview</h2>
        <button
          onClick={handleCalculateRisks}
          className="btn-primary"
          disabled={calculating}
        >
          {calculating ? 'Calculating...' : 'Recalculate All Risks'}
        </button>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-4" style={{ marginBottom: '2rem' }}>
        <div className="stat-card">
          <h3>Total Athletes</h3>
          <div className="stat-value">{overview.total_athletes}</div>
        </div>
        <div className="stat-card green">
          <h3>Low Risk</h3>
          <div className="stat-value">{overview.low_risk_count}</div>
        </div>
        <div className="stat-card yellow">
          <h3>Medium Risk</h3>
          <div className="stat-value">{overview.medium_risk_count}</div>
        </div>
        <div className="stat-card red">
          <h3>High Risk</h3>
          <div className="stat-value">{overview.high_risk_count}</div>
        </div>
      </div>

      {/* Filter */}
      <div className="card" style={{ marginBottom: '1rem' }}>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <strong>Filter by Risk Level:</strong>
          <button
            onClick={() => setRiskFilter(null)}
            className={riskFilter === null ? 'btn-primary' : 'btn-secondary'}
          >
            All
          </button>
          <button
            onClick={() => setRiskFilter('high')}
            className={riskFilter === 'high' ? 'btn-danger' : 'btn-secondary'}
          >
            High Risk
          </button>
          <button
            onClick={() => setRiskFilter('medium')}
            className={riskFilter === 'medium' ? 'btn-primary' : 'btn-secondary'}
          >
            Medium Risk
          </button>
          <button
            onClick={() => setRiskFilter('low')}
            className={riskFilter === 'low' ? 'btn-success' : 'btn-secondary'}
          >
            Low Risk
          </button>
        </div>
      </div>

      {/* Athletes Table */}
      <div className="card">
        <h3 className="card-header">Athletes</h3>
        {overview.athletes.length === 0 ? (
          <p style={{ textAlign: 'center', padding: '2rem', color: '#95a5a6' }}>
            No athletes found. Add athletes to get started.
          </p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Position</th>
                <th>Risk Level</th>
                <th>Risk Score</th>
                <th>ACWR</th>
                <th>Last Assessment</th>
              </tr>
            </thead>
            <tbody>
              {overview.athletes.map((athlete) => (
                <tr
                  key={athlete.id}
                  onClick={() => navigate(`/athlete/${athlete.id}`)}
                >
                  <td><strong>{athlete.name}</strong></td>
                  <td>{athlete.position || '-'}</td>
                  <td>
                    <span className={`risk-badge ${getRiskClass(athlete.risk_level)}`}>
                      {athlete.risk_level}
                    </span>
                  </td>
                  <td>{athlete.risk_score.toFixed(1)}</td>
                  <td>{athlete.acwr ? athlete.acwr.toFixed(2) : '-'}</td>
                  <td>{athlete.last_assessment_date || '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default TeamDashboard;
