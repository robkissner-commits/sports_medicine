import React, { useState, useEffect } from 'react';
import { getAthletes, createAthlete, deleteAthlete, uploadAthletes } from '../services/api';

function AthleteManagement() {
  const [athletes, setAthletes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [showUpload, setShowUpload] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState(null);
  const [file, setFile] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    position: '',
    age: '',
    email: '',
    team: ''
  });

  useEffect(() => {
    loadAthletes();
  }, []);

  const loadAthletes = async () => {
    try {
      setLoading(true);
      const response = await getAthletes();
      setAthletes(response.data);
    } catch (err) {
      setError('Failed to load athletes: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const submitData = {
        ...formData,
        age: formData.age ? parseInt(formData.age) : null,
      };
      await createAthlete(submitData);
      alert('Athlete created successfully!');
      setFormData({ name: '', position: '', age: '', email: '', team: '' });
      setShowForm(false);
      loadAthletes();
    } catch (err) {
      alert('Failed to create athlete: ' + err.message);
    }
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setUploadResult(null);
  };

  const handleUpload = async () => {
    if (!file) {
      alert('Please select a CSV file');
      return;
    }

    try {
      setUploading(true);
      setUploadResult(null);
      const response = await uploadAthletes(file);
      setUploadResult(response.data);
      setFile(null);
      document.getElementById('athlete-file-input').value = '';
      loadAthletes();
    } catch (err) {
      alert('Upload failed: ' + (err.response?.data?.detail || err.message));
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (id, name) => {
    if (window.confirm(`Are you sure you want to delete ${name}? This will delete all associated data.`)) {
      try {
        await deleteAthlete(id);
        alert('Athlete deleted successfully!');
        loadAthletes();
      } catch (err) {
        alert('Failed to delete athlete: ' + err.message);
      }
    }
  };

  if (loading) {
    return <div className="loading">Loading athletes...</div>;
  }

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '2rem', flexWrap: 'wrap', gap: '1rem' }}>
        <h2>Athlete Management</h2>
        <div style={{ display: 'flex', gap: '1rem' }}>
          <button
            onClick={() => {
              setShowUpload(!showUpload);
              setShowForm(false);
            }}
            className="btn-primary"
          >
            {showUpload ? 'Cancel Upload' : '📤 Upload CSV'}
          </button>
          <button
            onClick={() => {
              setShowForm(!showForm);
              setShowUpload(false);
            }}
            className="btn-primary"
          >
            {showForm ? 'Cancel' : '+ Add Athlete'}
          </button>
        </div>
      </div>

      {error && <div className="error">{error}</div>}

      {/* CSV Upload Section */}
      {showUpload && (
        <div className="card" style={{ marginBottom: '2rem' }}>
          <h3 className="card-header">Upload Athletes from CSV</h3>

          <div style={{ marginBottom: '1.5rem' }}>
            <p style={{ marginBottom: '1rem' }}>
              Upload a CSV file with athlete information. The file should contain:
            </p>
            <ul style={{ marginLeft: '1.5rem', lineHeight: '1.8' }}>
              <li><strong>name</strong> (required) - Athlete's full name</li>
              <li><strong>position</strong> (optional) - Playing position</li>
              <li><strong>age</strong> (optional) - Age in years</li>
              <li><strong>email</strong> (optional) - Email address</li>
              <li><strong>team</strong> (optional) - Team name</li>
            </ul>
          </div>

          <div className="form-group">
            <label>Select CSV File</label>
            <input
              id="athlete-file-input"
              type="file"
              accept=".csv,.xlsx"
              onChange={handleFileChange}
              style={{ padding: '0.75rem', fontSize: '1rem' }}
            />
          </div>

          <button
            onClick={handleUpload}
            disabled={uploading || !file}
            className="btn-success"
          >
            {uploading ? 'Uploading...' : 'Upload Athletes'}
          </button>

          {uploadResult && (
            <div style={{ marginTop: '1.5rem', padding: '1rem', backgroundColor: '#d4edda', borderRadius: '6px', border: '1px solid #c3e6cb' }}>
              <h4 style={{ color: '#155724', marginBottom: '0.5rem' }}>Upload Results</h4>
              <p><strong>Message:</strong> {uploadResult.message}</p>
              <p><strong>Created:</strong> {uploadResult.created_count} athletes</p>
              <p><strong>Updated:</strong> {uploadResult.updated_count} athletes</p>
              {uploadResult.skipped_count > 0 && (
                <p><strong>Skipped:</strong> {uploadResult.skipped_count} rows</p>
              )}
              {uploadResult.errors && uploadResult.errors.length > 0 && (
                <div>
                  <p style={{ marginTop: '1rem' }}><strong>Errors:</strong></p>
                  <ul style={{ marginLeft: '1.5rem', color: '#721c24' }}>
                    {uploadResult.errors.map((error, idx) => (
                      <li key={idx}>{error}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}

          <div style={{ marginTop: '1.5rem', padding: '1rem', backgroundColor: '#e7f3ff', borderRadius: '6px', border: '1px solid #bee5eb' }}>
            <h4 style={{ marginBottom: '0.5rem' }}>Example CSV Format:</h4>
            <pre style={{ backgroundColor: '#fff', padding: '0.75rem', borderRadius: '4px', overflow: 'auto' }}>
{`name,position,age,email,team
John Smith,Forward,24,john@team.com,Varsity
Sarah Johnson,Midfielder,22,sarah@team.com,Varsity
Mike Williams,Defender,25,mike@team.com,Varsity`}
            </pre>
            <p style={{ marginTop: '0.5rem', fontSize: '0.875rem', color: '#004085' }}>
              💡 Tip: If an athlete with the same name already exists, their information will be updated.
            </p>
          </div>
        </div>
      )}

      {/* Individual Add Form */}
      {showForm && (
        <div className="card" style={{ marginBottom: '2rem' }}>
          <h3 className="card-header">Add New Athlete</h3>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Name *</label>
              <input
                type="text"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                required
              />
            </div>

            <div className="form-group">
              <label>Position</label>
              <input
                type="text"
                value={formData.position}
                onChange={(e) => setFormData({ ...formData, position: e.target.value })}
              />
            </div>

            <div className="form-group">
              <label>Age</label>
              <input
                type="number"
                value={formData.age}
                onChange={(e) => setFormData({ ...formData, age: e.target.value })}
              />
            </div>

            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              />
            </div>

            <div className="form-group">
              <label>Team</label>
              <input
                type="text"
                value={formData.team}
                onChange={(e) => setFormData({ ...formData, team: e.target.value })}
              />
            </div>

            <button type="submit" className="btn-success">Create Athlete</button>
          </form>
        </div>
      )}

      {/* Athletes List */}
      <div className="card">
        <h3 className="card-header">Athletes ({athletes.length})</h3>
        {athletes.length === 0 ? (
          <p style={{ textAlign: 'center', padding: '2rem', color: '#95a5a6' }}>
            No athletes yet. Click "Upload CSV" or "Add Athlete" to get started.
          </p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Position</th>
                <th>Age</th>
                <th>Team</th>
                <th>Email</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {athletes.map((athlete) => (
                <tr key={athlete.id}>
                  <td><strong>{athlete.name}</strong></td>
                  <td>{athlete.position || '-'}</td>
                  <td>{athlete.age || '-'}</td>
                  <td>{athlete.team || '-'}</td>
                  <td>{athlete.email || '-'}</td>
                  <td>
                    <button
                      onClick={() => handleDelete(athlete.id, athlete.name)}
                      className="btn-danger"
                      style={{ padding: '0.5rem 1rem', fontSize: '0.875rem' }}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default AthleteManagement;
