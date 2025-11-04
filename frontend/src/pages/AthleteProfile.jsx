import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer, ReferenceLine
} from 'recharts';
import {
  getAthlete,
  getAthleteTrainingLoads,
  getAthleteTreatments,
  getAthleteInjuries,
  getAthleteLifestyleLogs,
  getAthleteRiskHistory,
  updateTrainingLoad,
  deleteTrainingLoad,
  updateTreatment,
  deleteTreatment,
  updateInjury,
  deleteInjury,
  updateLifestyleLog,
  deleteLifestyleLog,
  getAthleteACWRTrend,
  getAthleteTrainingSummary,
  calculateAthleteRisk,
  getInjuryRecoveryPrediction,
} from '../services/api';
import RiskBreakdown from '../components/RiskBreakdown';
import '../styles/AthleteProfile.css';

const AthleteProfile = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [athlete, setAthlete] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');
  const [trainingLoads, setTrainingLoads] = useState([]);
  const [treatments, setTreatments] = useState([]);
  const [injuries, setInjuries] = useState([]);
  const [lifestyleLogs, setLifestyleLogs] = useState([]);
  const [acwrData, setAcwrData] = useState([]);
  const [trainingSummary, setTrainingSummary] = useState(null);
  const [riskHistory, setRiskHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editingItem, setEditingItem] = useState(null);
  const [editFormData, setEditFormData] = useState({});
  const [recoveryPredictions, setRecoveryPredictions] = useState({});

  useEffect(() => {
    loadAthleteData();
  }, [id]);

  const loadAthleteData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Load athlete details
      const athleteResponse = await getAthlete(id);
      setAthlete(athleteResponse.data);

      // Load all historical data
      const [loadsRes, treatmentsRes, injuriesRes, lifestyleRes, acwrRes, summaryRes, riskRes] = await Promise.all([
        getAthleteTrainingLoads(id),
        getAthleteTreatments(id),
        getAthleteInjuries(id),
        getAthleteLifestyleLogs(id),
        getAthleteACWRTrend(id),
        getAthleteTrainingSummary(id),
        getAthleteRiskHistory(id),
      ]);

      setTrainingLoads(loadsRes.data);
      setTreatments(treatmentsRes.data);
      setInjuries(injuriesRes.data);
      setLifestyleLogs(lifestyleRes.data);
      setAcwrData(acwrRes.data);
      setTrainingSummary(summaryRes.data);
      setRiskHistory(riskRes.data);
    } catch (err) {
      setError(err.message || 'Failed to load athlete data');
      console.error('Error loading athlete data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (item, type) => {
    setEditingItem({ ...item, type });
    setEditFormData(item);
  };

  const handleCancelEdit = () => {
    setEditingItem(null);
    setEditFormData({});
  };

  const handleSaveEdit = async () => {
    try {
      const { id, type, athlete_id, created_at, ...updateData } = editFormData;

      switch (editingItem.type) {
        case 'trainingLoad':
          await updateTrainingLoad(editingItem.id, updateData);
          const loadsRes = await getAthleteTrainingLoads(athlete.id);
          setTrainingLoads(loadsRes.data);
          break;
        case 'treatment':
          await updateTreatment(editingItem.id, updateData);
          const treatmentsRes = await getAthleteTreatments(athlete.id);
          setTreatments(treatmentsRes.data);
          break;
        case 'injury':
          await updateInjury(editingItem.id, updateData);
          const injuriesRes = await getAthleteInjuries(athlete.id);
          setInjuries(injuriesRes.data);
          break;
        case 'lifestyle':
          await updateLifestyleLog(editingItem.id, updateData);
          const lifestyleRes = await getAthleteLifestyleLogs(athlete.id);
          setLifestyleLogs(lifestyleRes.data);
          break;
      }

      setEditingItem(null);
      setEditFormData({});
      alert('Record updated successfully!');
    } catch (err) {
      alert(`Failed to update record: ${err.message}`);
      console.error('Error updating record:', err);
    }
  };

  const handleDelete = async (itemId, type) => {
    if (!window.confirm('Are you sure you want to delete this record?')) {
      return;
    }

    try {
      switch (type) {
        case 'trainingLoad':
          await deleteTrainingLoad(itemId);
          const loadsRes = await getAthleteTrainingLoads(athlete.id);
          setTrainingLoads(loadsRes.data);
          break;
        case 'treatment':
          await deleteTreatment(itemId);
          const treatmentsRes = await getAthleteTreatments(athlete.id);
          setTreatments(treatmentsRes.data);
          break;
        case 'injury':
          await deleteInjury(itemId);
          const injuriesRes = await getAthleteInjuries(athlete.id);
          setInjuries(injuriesRes.data);
          break;
        case 'lifestyle':
          await deleteLifestyleLog(itemId);
          const lifestyleRes = await getAthleteLifestyleLogs(athlete.id);
          setLifestyleLogs(lifestyleRes.data);
          break;
      }

      alert('Record deleted successfully!');
    } catch (err) {
      alert(`Failed to delete record: ${err.message}`);
      console.error('Error deleting record:', err);
    }
  };

  const handleRecalculateRisk = async () => {
    try {
      await calculateAthleteRisk(athlete.id);
      alert('Risk recalculated successfully!');
      loadAthleteData();
    } catch (err) {
      alert(`Failed to recalculate risk: ${err.message}`);
    }
  };

  const handleViewRecoveryPrediction = async (injuryId) => {
    try {
      const response = await getInjuryRecoveryPrediction(injuryId);
      setRecoveryPredictions(prev => ({
        ...prev,
        [injuryId]: response.data
      }));
    } catch (err) {
      alert(`Failed to fetch recovery prediction: ${err.message}`);
      console.error('Error fetching recovery prediction:', err);
    }
  };

  if (loading) {
    return <div className="loading">Loading athlete data...</div>;
  }

  if (error) {
    return (
      <div className="error-container">
        <h2>Error Loading Data</h2>
        <p>{error}</p>
        <button onClick={() => navigate('/dashboard')}>Back to Dashboard</button>
      </div>
    );
  }

  if (!athlete) {
    return <div className="error-container">Athlete not found</div>;
  }

  const getRiskColor = (riskLevel) => {
    if (!riskLevel) return '#999';
    switch (riskLevel.toLowerCase()) {
      case 'high':
        return '#dc3545';
      case 'medium':
        return '#ffc107';
      case 'low':
        return '#28a745';
      default:
        return '#999';
    }
  };

  return (
    <div className="athlete-profile">
      <div className="profile-header">
        <button onClick={() => navigate('/dashboard')} className="back-button">
          ← Back to Dashboard
        </button>
        <h1>{athlete.name}</h1>
        <div className="athlete-info">
          {athlete.position && <span className="info-badge">Position: {athlete.position}</span>}
          {athlete.age && <span className="info-badge">Age: {athlete.age}</span>}
          {athlete.team && <span className="info-badge">Team: {athlete.team}</span>}
          {athlete.email && <span className="info-badge">Email: {athlete.email}</span>}
        </div>
      </div>

      <div className="tabs">
        <button
          className={activeTab === 'overview' ? 'active' : ''}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button
          className={activeTab === 'training' ? 'active' : ''}
          onClick={() => setActiveTab('training')}
        >
          Training Loads ({trainingLoads.length})
        </button>
        <button
          className={activeTab === 'treatments' ? 'active' : ''}
          onClick={() => setActiveTab('treatments')}
        >
          Treatments ({treatments.length})
        </button>
        <button
          className={activeTab === 'injuries' ? 'active' : ''}
          onClick={() => setActiveTab('injuries')}
        >
          Injuries ({injuries.length})
        </button>
        <button
          className={activeTab === 'lifestyle' ? 'active' : ''}
          onClick={() => setActiveTab('lifestyle')}
        >
          Lifestyle ({lifestyleLogs.length})
        </button>
      </div>

      <div className="tab-content">
        {activeTab === 'overview' && (
          <div className="overview-tab">
            <div className="stats-grid">
              <div className="stat-card" style={{ borderLeft: `4px solid ${getRiskColor(athlete.risk_level)}` }}>
                <h3>Current Risk Level</h3>
                <div className="stat-value" style={{ color: getRiskColor(athlete.risk_level) }}>
                  {athlete.risk_level || 'Not Calculated'}
                </div>
                <button onClick={handleRecalculateRisk} className="btn-primary">
                  Recalculate Risk
                </button>
              </div>

              <div className="stat-card">
                <h3>Current ACWR</h3>
                <div className="stat-value">
                  {athlete.acwr ? athlete.acwr.toFixed(2) : 'N/A'}
                </div>
                <p className="stat-description">Acute:Chronic Workload Ratio</p>
              </div>

              <div className="stat-card">
                <h3>Risk Score</h3>
                <div className="stat-value">
                  {athlete.risk_score ? athlete.risk_score.toFixed(1) : 'N/A'}
                </div>
                <p className="stat-description">Out of 100</p>
              </div>

              {trainingSummary && (
                <>
                  <div className="stat-card">
                    <h3>7-Day Avg Load</h3>
                    <div className="stat-value">
                      {trainingSummary.acute_load?.toFixed(1) || 'N/A'}
                    </div>
                  </div>

                  <div className="stat-card">
                    <h3>28-Day Avg Load</h3>
                    <div className="stat-value">
                      {trainingSummary.chronic_load?.toFixed(1) || 'N/A'}
                    </div>
                  </div>

                  <div className="stat-card">
                    <h3>Total Distance (28d)</h3>
                    <div className="stat-value">
                      {trainingSummary.total_distance?.toFixed(0) || 'N/A'} m
                    </div>
                  </div>
                </>
              )}
            </div>

            <div className="data-summary">
              <h3>Data Summary</h3>
              <ul>
                <li>Total Training Sessions: {trainingLoads.length}</li>
                <li>Total Treatments: {treatments.length}</li>
                <li>Injury History: {injuries.length} recorded injuries</li>
                <li>Lifestyle Logs: {lifestyleLogs.length} entries</li>
              </ul>
            </div>

            {/* ACWR Trend Chart */}
            {acwrData && acwrData.data && acwrData.data.length > 0 && (
              <div className="chart-container">
                <h3>ACWR Trend (8 Weeks)</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={acwrData.data}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <ReferenceLine y={1.5} stroke="#dc3545" strokeDasharray="3 3" label="High Risk (>1.5)" />
                    <ReferenceLine y={0.8} stroke="#dc3545" strokeDasharray="3 3" label="High Risk (<0.8)" />
                    <ReferenceLine y={1.0} stroke="#28a745" strokeDasharray="3 3" label="Optimal (1.0)" />
                    <Line type="monotone" dataKey="acwr" stroke="#007bff" strokeWidth={2} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            )}

            {/* Training Load Chart */}
            {trainingSummary && trainingSummary.loads_by_date && trainingSummary.loads_by_date.length > 0 && (
              <div className="chart-container">
                <h3>Training Load (28 Days)</h3>
                <p className="chart-description">
                  {trainingSummary.session_count} sessions •
                  Avg Load: {trainingSummary.average_load?.toFixed(1)} •
                  Total Distance: {trainingSummary.total_distance ? (trainingSummary.total_distance / 1000).toFixed(2) : 'N/A'} km
                </p>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={trainingSummary.loads_by_date}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="training_load" fill="#007bff" name="Training Load" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            )}

            {/* Risk History Chart */}
            {riskHistory.length > 0 && (
              <div className="chart-container">
                <h3>Risk Assessment History</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={riskHistory.slice(-30)}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="overall_risk_score" stroke="#dc3545" name="Risk Score" strokeWidth={2} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            )}

            {/* Enhanced Risk Breakdown */}
            {riskHistory.length > 0 && (
              <RiskBreakdown riskData={riskHistory[riskHistory.length - 1]} />
            )}
          </div>
        )}

        {activeTab === 'training' && (
          <div className="training-tab">
            <h2>Training Load History</h2>
            {trainingLoads.length === 0 ? (
              <p>No training load data available.</p>
            ) : (
              <div className="data-table">
                <table>
                  <thead>
                    <tr>
                      <th>Date</th>
                      <th>Distance (mi)</th>
                      <th>Accel Load</th>
                      <th>Avg Speed (mph)</th>
                      <th>Max Speed (mph)</th>
                      <th>Calculated Load</th>
                      <th>Session Type</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {trainingLoads.map((load) => (
                      <tr key={load.id}>
                        {editingItem?.id === load.id ? (
                          <>
                            <td>
                              <input
                                type="date"
                                value={editFormData.date}
                                onChange={(e) => setEditFormData({ ...editFormData, date: e.target.value })}
                              />
                            </td>
                            <td>
                              <input
                                type="number"
                                step="0.1"
                                value={editFormData.distance_miles || ''}
                                onChange={(e) => setEditFormData({ ...editFormData, distance_miles: e.target.value ? parseFloat(e.target.value) : null })}
                                placeholder="Miles"
                              />
                            </td>
                            <td>
                              <input
                                type="number"
                                step="0.1"
                                value={editFormData.accumulated_accel_load || ''}
                                onChange={(e) => setEditFormData({ ...editFormData, accumulated_accel_load: e.target.value ? parseFloat(e.target.value) : null })}
                                placeholder="Accel Load"
                              />
                            </td>
                            <td>
                              <input
                                type="number"
                                step="0.1"
                                value={editFormData.average_speed_mph || ''}
                                onChange={(e) => setEditFormData({ ...editFormData, average_speed_mph: e.target.value ? parseFloat(e.target.value) : null })}
                                placeholder="Avg mph"
                              />
                            </td>
                            <td>
                              <input
                                type="number"
                                step="0.1"
                                value={editFormData.max_speed_mph || ''}
                                onChange={(e) => setEditFormData({ ...editFormData, max_speed_mph: e.target.value ? parseFloat(e.target.value) : null })}
                                placeholder="Max mph"
                              />
                            </td>
                            <td>
                              <span style={{color: '#6c757d', fontStyle: 'italic'}}>Auto-calculated</span>
                            </td>
                            <td>
                              <input
                                type="text"
                                value={editFormData.session_type || ''}
                                onChange={(e) => setEditFormData({ ...editFormData, session_type: e.target.value })}
                                placeholder="Training"
                              />
                            </td>
                            <td>
                              <button onClick={handleSaveEdit} className="btn-save">Save</button>
                              <button onClick={handleCancelEdit} className="btn-cancel">Cancel</button>
                            </td>
                          </>
                        ) : (
                          <>
                            <td>{load.date}</td>
                            <td>{load.distance_miles?.toFixed(1) || '-'}</td>
                            <td>{load.accumulated_accel_load?.toFixed(1) || '-'}</td>
                            <td>{load.average_speed_mph?.toFixed(1) || '-'}</td>
                            <td>{load.max_speed_mph?.toFixed(1) || '-'}</td>
                            <td><strong>{load.training_load?.toFixed(0)}</strong></td>
                            <td>{load.session_type || '-'}</td>
                            <td>
                              <button onClick={() => handleEdit(load, 'trainingLoad')} className="btn-edit">Edit</button>
                              <button onClick={() => handleDelete(load.id, 'trainingLoad')} className="btn-delete">Delete</button>
                            </td>
                          </>
                        )}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}

        {activeTab === 'treatments' && (
          <div className="treatments-tab">
            <h2>Treatment History</h2>
            {treatments.length === 0 ? (
              <p>No treatment data available.</p>
            ) : (
              <div className="data-table">
                <table>
                  <thead>
                    <tr>
                      <th>Date</th>
                      <th>Modality</th>
                      <th>Body Part</th>
                      <th>Duration (min)</th>
                      <th>Severity</th>
                      <th>Notes</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {treatments.map((treatment) => (
                      <tr key={treatment.id}>
                        {editingItem?.id === treatment.id ? (
                          <>
                            <td>
                              <input
                                type="date"
                                value={editFormData.date}
                                onChange={(e) => setEditFormData({ ...editFormData, date: e.target.value })}
                              />
                            </td>
                            <td>
                              <input
                                type="text"
                                value={editFormData.modality}
                                onChange={(e) => setEditFormData({ ...editFormData, modality: e.target.value })}
                              />
                            </td>
                            <td>
                              <input
                                type="text"
                                value={editFormData.body_part || ''}
                                onChange={(e) => setEditFormData({ ...editFormData, body_part: e.target.value })}
                              />
                            </td>
                            <td>
                              <input
                                type="number"
                                value={editFormData.duration || ''}
                                onChange={(e) => setEditFormData({ ...editFormData, duration: e.target.value ? parseInt(e.target.value) : null })}
                              />
                            </td>
                            <td>
                              <input
                                type="text"
                                value={editFormData.severity || ''}
                                onChange={(e) => setEditFormData({ ...editFormData, severity: e.target.value })}
                              />
                            </td>
                            <td>
                              <input
                                type="text"
                                value={editFormData.notes || ''}
                                onChange={(e) => setEditFormData({ ...editFormData, notes: e.target.value })}
                              />
                            </td>
                            <td>
                              <button onClick={handleSaveEdit} className="btn-save">Save</button>
                              <button onClick={handleCancelEdit} className="btn-cancel">Cancel</button>
                            </td>
                          </>
                        ) : (
                          <>
                            <td>{treatment.date}</td>
                            <td>{treatment.modality}</td>
                            <td>{treatment.body_part || '-'}</td>
                            <td>{treatment.duration || '-'}</td>
                            <td>{treatment.severity || '-'}</td>
                            <td>{treatment.notes || '-'}</td>
                            <td>
                              <button onClick={() => handleEdit(treatment, 'treatment')} className="btn-edit">Edit</button>
                              <button onClick={() => handleDelete(treatment.id, 'treatment')} className="btn-delete">Delete</button>
                            </td>
                          </>
                        )}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}

        {activeTab === 'injuries' && (
          <div className="injuries-tab">
            <h2>Injury History</h2>
            {injuries.length === 0 ? (
              <p>No injury data available.</p>
            ) : (
              <div className="data-table">
                <table>
                  <thead>
                    <tr>
                      <th>Injury Date</th>
                      <th>Type</th>
                      <th>Body Part</th>
                      <th>Severity</th>
                      <th>Recovery Date</th>
                      <th>Days Missed</th>
                      <th>Description</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {injuries.map((injury) => (
                      <tr key={injury.id}>
                        {editingItem?.id === injury.id ? (
                          <>
                            <td>
                              <input
                                type="date"
                                value={editFormData.injury_date}
                                onChange={(e) => setEditFormData({ ...editFormData, injury_date: e.target.value })}
                              />
                            </td>
                            <td>
                              <input
                                type="text"
                                value={editFormData.injury_type}
                                onChange={(e) => setEditFormData({ ...editFormData, injury_type: e.target.value })}
                              />
                            </td>
                            <td>
                              <input
                                type="text"
                                value={editFormData.body_part}
                                onChange={(e) => setEditFormData({ ...editFormData, body_part: e.target.value })}
                              />
                            </td>
                            <td>
                              <input
                                type="text"
                                value={editFormData.severity || ''}
                                onChange={(e) => setEditFormData({ ...editFormData, severity: e.target.value })}
                              />
                            </td>
                            <td>
                              <input
                                type="date"
                                value={editFormData.recovery_date || ''}
                                onChange={(e) => setEditFormData({ ...editFormData, recovery_date: e.target.value })}
                              />
                            </td>
                            <td>
                              <input
                                type="number"
                                value={editFormData.days_missed || ''}
                                onChange={(e) => setEditFormData({ ...editFormData, days_missed: e.target.value ? parseInt(e.target.value) : null })}
                              />
                            </td>
                            <td>
                              <input
                                type="text"
                                value={editFormData.description || ''}
                                onChange={(e) => setEditFormData({ ...editFormData, description: e.target.value })}
                              />
                            </td>
                            <td>
                              <button onClick={handleSaveEdit} className="btn-save">Save</button>
                              <button onClick={handleCancelEdit} className="btn-cancel">Cancel</button>
                            </td>
                          </>
                        ) : (
                          <>
                            <td>{injury.injury_date}</td>
                            <td>{injury.injury_type}</td>
                            <td>{injury.body_part}</td>
                            <td>{injury.severity || '-'}</td>
                            <td>{injury.recovery_date || '-'}</td>
                            <td>{injury.days_missed || '-'}</td>
                            <td>{injury.description || '-'}</td>
                            <td>
                              <button onClick={() => handleEdit(injury, 'injury')} className="btn-edit">Edit</button>
                              <button onClick={() => handleDelete(injury.id, 'injury')} className="btn-delete">Delete</button>
                              <button onClick={() => handleViewRecoveryPrediction(injury.id)} className="btn-info">
                                {recoveryPredictions[injury.id] ? 'Refresh' : 'Predict Recovery'}
                              </button>
                            </td>
                          </>
                        )}
                      </tr>
                    ))}
                  </tbody>
                </table>

                {/* Recovery Predictions */}
                {Object.keys(recoveryPredictions).length > 0 && (
                  <div className="recovery-predictions">
                    <h3>Recovery Predictions (Evidence-Based)</h3>
                    {injuries.filter(inj => recoveryPredictions[inj.id]).map((injury) => {
                      const pred = recoveryPredictions[injury.id];
                      return (
                        <div key={injury.id} className="recovery-card">
                          <h4>{injury.injury_type} - {injury.body_part}</h4>
                          <div className="recovery-timeline">
                            <div className="timeline-item">
                              <span className="timeline-label">Best Case:</span>
                              <span className="timeline-value">{pred.min_recovery_days} days</span>
                              <span className="timeline-date">({new Date(pred.expected_return_date_min).toLocaleDateString()})</span>
                            </div>
                            <div className="timeline-item typical">
                              <span className="timeline-label">Most Likely:</span>
                              <span className="timeline-value">{pred.typical_recovery_days} days</span>
                              <span className="timeline-date">({new Date(pred.expected_return_date_typical).toLocaleDateString()})</span>
                            </div>
                            <div className="timeline-item">
                              <span className="timeline-label">Worst Case:</span>
                              <span className="timeline-value">{pred.max_recovery_days} days</span>
                              <span className="timeline-date">({new Date(pred.expected_return_date_max).toLocaleDateString()})</span>
                            </div>
                          </div>
                          {pred.modifiers_applied && (
                            <div className="recovery-modifiers">
                              <h5>Factors Affecting Recovery:</h5>
                              <div className="modifiers-list">
                                {pred.modifiers_applied.age_factor > 1.0 && (
                                  <span className="modifier-tag">Age: +{((pred.modifiers_applied.age_factor - 1) * 100).toFixed(0)}%</span>
                                )}
                                {pred.modifiers_applied.severity_factor > 1.0 && (
                                  <span className="modifier-tag">Severity: +{((pred.modifiers_applied.severity_factor - 1) * 100).toFixed(0)}%</span>
                                )}
                                {pred.modifiers_applied.previous_injury_factor > 1.0 && (
                                  <span className="modifier-tag">Previous Injury: +{((pred.modifiers_applied.previous_injury_factor - 1) * 100).toFixed(0)}%</span>
                                )}
                                <span className="modifier-tag total">Total Modifier: {pred.modifiers_applied.total_multiplier}×</span>
                              </div>
                            </div>
                          )}

                          {pred.justification && (
                            <div className="recovery-justification">
                              <h5>Clinical Justification:</h5>
                              <div className="justification-text">
                                {pred.justification.split('\n').map((line, idx) => (
                                  <p key={idx}>{line}</p>
                                ))}
                              </div>
                            </div>
                          )}

                          {pred.research_links && pred.research_links.length > 0 && (
                            <div className="research-links">
                              <h5>Supporting Research:</h5>
                              <div className="links-list">
                                {pred.research_links.map((link, idx) => (
                                  <div key={idx} className="research-link-item">
                                    <strong>{link.title}</strong>
                                    <p className="citation">{link.citation}</p>
                                    <div className="link-actions">
                                      {link.url && (
                                        <a href={link.url} target="_blank" rel="noopener noreferrer" className="research-link-btn">
                                          View Full Study
                                        </a>
                                      )}
                                      {link.doi && (
                                        <a href={`https://doi.org/${link.doi}`} target="_blank" rel="noopener noreferrer" className="research-link-btn doi">
                                          DOI: {link.doi}
                                        </a>
                                      )}
                                    </div>
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {activeTab === 'lifestyle' && (
          <div className="lifestyle-tab">
            <h2>Lifestyle Log History</h2>
            {lifestyleLogs.length === 0 ? (
              <p>No lifestyle data available.</p>
            ) : (
              <div className="data-table">
                <table>
                  <thead>
                    <tr>
                      <th>Date</th>
                      <th>Sleep (hrs)</th>
                      <th>Sleep Quality</th>
                      <th>Nutrition</th>
                      <th>Hydration (L)</th>
                      <th>Stress</th>
                      <th>Soreness</th>
                      <th>Fatigue</th>
                      <th>Notes</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {lifestyleLogs.map((log) => (
                      <tr key={log.id}>
                        {editingItem?.id === log.id ? (
                          <>
                            <td>
                              <input
                                type="date"
                                value={editFormData.date}
                                onChange={(e) => setEditFormData({ ...editFormData, date: e.target.value })}
                              />
                            </td>
                            <td>
                              <input
                                type="number"
                                step="0.5"
                                value={editFormData.sleep_hours || ''}
                                onChange={(e) => setEditFormData({ ...editFormData, sleep_hours: e.target.value ? parseFloat(e.target.value) : null })}
                              />
                            </td>
                            <td>
                              <input
                                type="number"
                                min="1"
                                max="10"
                                value={editFormData.sleep_quality || ''}
                                onChange={(e) => setEditFormData({ ...editFormData, sleep_quality: e.target.value ? parseInt(e.target.value) : null })}
                              />
                            </td>
                            <td>
                              <input
                                type="number"
                                min="1"
                                max="10"
                                value={editFormData.nutrition_score || ''}
                                onChange={(e) => setEditFormData({ ...editFormData, nutrition_score: e.target.value ? parseInt(e.target.value) : null })}
                              />
                            </td>
                            <td>
                              <input
                                type="number"
                                step="0.1"
                                value={editFormData.hydration_liters || ''}
                                onChange={(e) => setEditFormData({ ...editFormData, hydration_liters: e.target.value ? parseFloat(e.target.value) : null })}
                              />
                            </td>
                            <td>
                              <input
                                type="number"
                                min="1"
                                max="10"
                                value={editFormData.stress_level || ''}
                                onChange={(e) => setEditFormData({ ...editFormData, stress_level: e.target.value ? parseInt(e.target.value) : null })}
                              />
                            </td>
                            <td>
                              <input
                                type="number"
                                min="1"
                                max="10"
                                value={editFormData.soreness_level || ''}
                                onChange={(e) => setEditFormData({ ...editFormData, soreness_level: e.target.value ? parseInt(e.target.value) : null })}
                              />
                            </td>
                            <td>
                              <input
                                type="number"
                                min="1"
                                max="10"
                                value={editFormData.fatigue_level || ''}
                                onChange={(e) => setEditFormData({ ...editFormData, fatigue_level: e.target.value ? parseInt(e.target.value) : null })}
                              />
                            </td>
                            <td>
                              <input
                                type="text"
                                value={editFormData.notes || ''}
                                onChange={(e) => setEditFormData({ ...editFormData, notes: e.target.value })}
                              />
                            </td>
                            <td>
                              <button onClick={handleSaveEdit} className="btn-save">Save</button>
                              <button onClick={handleCancelEdit} className="btn-cancel">Cancel</button>
                            </td>
                          </>
                        ) : (
                          <>
                            <td>{log.date}</td>
                            <td>{log.sleep_hours || '-'}</td>
                            <td>{log.sleep_quality || '-'}</td>
                            <td>{log.nutrition_score || '-'}</td>
                            <td>{log.hydration_liters || '-'}</td>
                            <td>{log.stress_level || '-'}</td>
                            <td>{log.soreness_level || '-'}</td>
                            <td>{log.fatigue_level || '-'}</td>
                            <td>{log.notes || '-'}</td>
                            <td>
                              <button onClick={() => handleEdit(log, 'lifestyle')} className="btn-edit">Edit</button>
                              <button onClick={() => handleDelete(log.id, 'lifestyle')} className="btn-delete">Delete</button>
                            </td>
                          </>
                        )}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default AthleteProfile;
