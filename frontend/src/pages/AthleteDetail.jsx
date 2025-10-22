import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer, ReferenceLine
} from 'recharts';
import {
  getAthlete,
  getAthleteACWRTrend,
  getAthleteTrainingSummary,
  getAthleteRiskHistory,
  calculateAthleteRisk
} from '../services/api';

function AthleteDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [athlete, setAthlete] = useState(null);
  const [acwrData, setAcwrData] = useState(null);
  const [trainingSummary, setTrainingSummary] = useState(null);
  const [riskHistory, setRiskHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadAthleteData();
  }, [id]);

  const loadAthleteData = async () => {
    try {
      setLoading(true);
      setError(null);

      const [athleteRes, acwrRes, summaryRes, riskRes] = await Promise.all([
        getAthlete(id),
        getAthleteACWRTrend(id, 56),
        getAthleteTrainingSummary(id, 28),
        getAthleteRiskHistory(id)
      ]);

      setAthlete(athleteRes.data);
      setAcwrData(acwrRes.data);
      setTrainingSummary(summaryRes.data);
      setRiskHistory(riskRes.data);
    } catch (err) {
      setError('Failed to load athlete data: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCalculateRisk = async () => {
    try {
      await calculateAthleteRisk(id);
      alert('Risk calculation completed!');
      loadAthleteData();
    } catch (err) {
      alert('Failed to calculate risk: ' + err.message);
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
    return <div className="loading">Loading athlete data...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  if (!athlete) {
    return <div className="error">Athlete not found</div>;
  }

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '2rem' }}>
        <div>
          <button onClick={() => navigate('/')} className="btn-secondary" style={{ marginBottom: '1rem' }}>
            ← Back to Dashboard
          </button>
          <h2>{athlete.name}</h2>
          <p style={{ color: '#7f8c8d' }}>
            {athlete.position && `${athlete.position} • `}
            {athlete.team && `${athlete.team} • `}
            {athlete.age && `Age: ${athlete.age}`}
          </p>
        </div>
        <button onClick={handleCalculateRisk} className="btn-primary">
          Recalculate Risk
        </button>
      </div>

      {/* Current Status */}
      <div className="grid grid-4" style={{ marginBottom: '2rem' }}>
        <div className="card">
          <h4 style={{ color: '#7f8c8d', marginBottom: '0.5rem' }}>Current Risk</h4>
          {athlete.current_risk_level ? (
            <span className={`risk-badge ${getRiskClass(athlete.current_risk_level)}`}>
              {athlete.current_risk_level}
            </span>
          ) : (
            <span>Not assessed</span>
          )}
          <div style={{ fontSize: '1.5rem', marginTop: '0.5rem' }}>
            {athlete.current_risk_score ? athlete.current_risk_score.toFixed(1) : '-'}
          </div>
        </div>

        <div className="card">
          <h4 style={{ color: '#7f8c8d', marginBottom: '0.5rem' }}>Current ACWR</h4>
          <div style={{ fontSize: '1.5rem' }}>
            {athlete.latest_acwr ? athlete.latest_acwr.toFixed(2) : '-'}
          </div>
          {athlete.latest_acwr && (
            <small style={{ color: athlete.latest_acwr > 1.5 || athlete.latest_acwr < 0.8 ? '#e74c3c' : '#27ae60' }}>
              {athlete.latest_acwr > 1.5 || athlete.latest_acwr < 0.8 ? 'High Risk Range' : 'Safe Range'}
            </small>
          )}
        </div>

        <div className="card">
          <h4 style={{ color: '#7f8c8d', marginBottom: '0.5rem' }}>Recent Injuries</h4>
          <div style={{ fontSize: '1.5rem' }}>{athlete.recent_injuries_count}</div>
          <small style={{ color: '#7f8c8d' }}>Last 6 months</small>
        </div>

        <div className="card">
          <h4 style={{ color: '#7f8c8d', marginBottom: '0.5rem' }}>Days Since Injury</h4>
          <div style={{ fontSize: '1.5rem' }}>
            {athlete.days_since_last_injury !== null ? athlete.days_since_last_injury : '-'}
          </div>
          <small style={{ color: '#7f8c8d' }}>Last injury</small>
        </div>
      </div>

      {/* ACWR Trend Chart */}
      {acwrData && acwrData.data && acwrData.data.length > 0 && (
        <div className="card" style={{ marginBottom: '2rem' }}>
          <h3 className="card-header">ACWR Trend (8 Weeks)</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={acwrData.data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <ReferenceLine y={1.5} stroke="#e74c3c" strokeDasharray="3 3" label="High Risk (>1.5)" />
              <ReferenceLine y={0.8} stroke="#e74c3c" strokeDasharray="3 3" label="High Risk (<0.8)" />
              <ReferenceLine y={1.0} stroke="#27ae60" strokeDasharray="3 3" label="Optimal (1.0)" />
              <Line type="monotone" dataKey="acwr" stroke="#3498db" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Training Load Chart */}
      {trainingSummary && trainingSummary.loads_by_date && trainingSummary.loads_by_date.length > 0 && (
        <div className="card" style={{ marginBottom: '2rem' }}>
          <h3 className="card-header">Training Load (28 Days)</h3>
          <div style={{ marginBottom: '1rem' }}>
            <strong>Summary:</strong> {trainingSummary.session_count} sessions •
            Avg Load: {trainingSummary.average_load.toFixed(1)} •
            Total Distance: {(trainingSummary.total_distance_meters / 1000).toFixed(2)} km
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={trainingSummary.loads_by_date}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="training_load" fill="#3498db" name="Training Load" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Risk History */}
      {riskHistory.length > 0 && (
        <div className="card">
          <h3 className="card-header">Risk Assessment History</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={riskHistory.slice(-30)}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="overall_risk_score" stroke="#e74c3c" name="Risk Score" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Latest Recommendations */}
      {riskHistory.length > 0 && riskHistory[riskHistory.length - 1].recommendations && (
        <div className="card" style={{ marginTop: '2rem' }}>
          <h3 className="card-header">Latest Recommendations</h3>
          <div style={{ whiteSpace: 'pre-line', lineHeight: '1.8' }}>
            {riskHistory[riskHistory.length - 1].recommendations}
          </div>
        </div>
      )}
    </div>
  );
}

export default AthleteDetail;
