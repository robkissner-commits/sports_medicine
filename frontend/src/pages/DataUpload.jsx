import React, { useState, useEffect } from 'react';
import { getAthletes, uploadTrainingLoads, uploadTreatments, uploadInjuries } from '../services/api';

function DataUpload() {
  const [athletes, setAthletes] = useState([]);
  const [selectedAthlete, setSelectedAthlete] = useState('');
  const [uploadType, setUploadType] = useState('training');
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState(null);

  useEffect(() => {
    loadAthletes();
  }, []);

  const loadAthletes = async () => {
    try {
      const response = await getAthletes();
      setAthletes(response.data);
    } catch (err) {
      console.error('Failed to load athletes:', err);
    }
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setResult(null);
  };

  const handleUpload = async () => {
    if (!file) {
      alert('Please select a file');
      return;
    }

    try {
      setUploading(true);
      setResult(null);

      const athleteId = selectedAthlete ? parseInt(selectedAthlete) : null;
      let response;

      switch (uploadType) {
        case 'training':
          response = await uploadTrainingLoads(file, athleteId);
          break;
        case 'treatments':
          response = await uploadTreatments(file, athleteId);
          break;
        case 'injuries':
          response = await uploadInjuries(file, athleteId);
          break;
        default:
          throw new Error('Invalid upload type');
      }

      setResult(response.data);
      setFile(null);
      document.getElementById('file-input').value = '';
    } catch (err) {
      alert('Upload failed: ' + (err.response?.data?.detail || err.message));
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <h2 style={{ marginBottom: '2rem' }}>Upload Data</h2>

      <div className="card" style={{ marginBottom: '2rem' }}>
        <h3 className="card-header">Select Data Type</h3>
        <div className="form-group">
          <label>Upload Type</label>
          <select
            value={uploadType}
            onChange={(e) => setUploadType(e.target.value)}
            style={{ padding: '0.75rem', fontSize: '1rem', borderRadius: '6px', border: '1px solid #dfe6e9' }}
          >
            <option value="training">Training Loads (Kinexon)</option>
            <option value="treatments">Treatments (ATS)</option>
            <option value="injuries">Injury History</option>
          </select>
        </div>

        <div className="form-group">
          <label>Athlete (Optional - leave blank if CSV contains athlete info)</label>
          <select
            value={selectedAthlete}
            onChange={(e) => setSelectedAthlete(e.target.value)}
            style={{ padding: '0.75rem', fontSize: '1rem', borderRadius: '6px', border: '1px solid #dfe6e9' }}
          >
            <option value="">Multiple Athletes / Auto-detect</option>
            {athletes.map((athlete) => (
              <option key={athlete.id} value={athlete.id}>
                {athlete.name}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label>CSV/Excel File</label>
          <input
            id="file-input"
            type="file"
            accept=".csv,.xlsx"
            onChange={handleFileChange}
            style={{ padding: '0.75rem', fontSize: '1rem' }}
          />
        </div>

        <button
          onClick={handleUpload}
          disabled={uploading || !file}
          className="btn-primary"
        >
          {uploading ? 'Uploading...' : 'Upload'}
        </button>
      </div>

      {result && (
        <div className="card">
          <h3 className="card-header" style={{ color: '#27ae60' }}>Upload Results</h3>
          <p><strong>Message:</strong> {result.message}</p>
          <p><strong>Records Created:</strong> {result.created_count}</p>
          {result.errors && result.errors.length > 0 && (
            <div>
              <p><strong>Errors ({result.errors.length}):</strong></p>
              <ul style={{ color: '#e74c3c', marginLeft: '1.5rem' }}>
                {result.errors.map((error, idx) => (
                  <li key={idx}>{error}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      <div className="card">
        <h3 className="card-header">File Format Guidelines</h3>

        <div style={{ marginBottom: '1.5rem' }}>
          <h4>Training Loads (Kinexon)</h4>
          <p>Required columns:</p>
          <ul style={{ marginLeft: '1.5rem', lineHeight: '1.8' }}>
            <li><code>date</code> - Date in YYYY-MM-DD format</li>
            <li><code>training_load</code> or <code>load</code> - Numeric training load value</li>
            <li><code>athlete_id</code> or <code>athlete_name</code> - If not specified above</li>
          </ul>
          <p>Optional columns:</p>
          <ul style={{ marginLeft: '1.5rem', lineHeight: '1.8' }}>
            <li><code>total_distance</code>, <code>high_speed_distance</code>, <code>sprint_distance</code></li>
            <li><code>accelerations</code>, <code>decelerations</code>, <code>max_speed</code></li>
            <li><code>duration</code>, <code>session_type</code>, <code>player_load</code></li>
          </ul>
        </div>

        <div style={{ marginBottom: '1.5rem' }}>
          <h4>Treatments (ATS)</h4>
          <p>Required columns:</p>
          <ul style={{ marginLeft: '1.5rem', lineHeight: '1.8' }}>
            <li><code>date</code> or <code>treatment_date</code></li>
            <li><code>modality</code> or <code>treatment_type</code> - Type of treatment</li>
            <li><code>athlete_id</code> or <code>athlete_name</code></li>
          </ul>
          <p>Optional: <code>duration</code>, <code>body_part</code>, <code>severity</code>, <code>notes</code></p>
        </div>

        <div>
          <h4>Injury History</h4>
          <p>Required columns:</p>
          <ul style={{ marginLeft: '1.5rem', lineHeight: '1.8' }}>
            <li><code>injury_date</code></li>
            <li><code>injury_type</code></li>
            <li><code>body_part</code></li>
            <li><code>athlete_id</code> or <code>athlete_name</code></li>
          </ul>
          <p>Optional: <code>severity</code>, <code>recovery_date</code>, <code>days_missed</code>, <code>description</code></p>
        </div>
      </div>
    </div>
  );
}

export default DataUpload;
