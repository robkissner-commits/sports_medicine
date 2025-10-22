import React, { useState, useEffect } from 'react';
import { getAthletes, createAthlete, deleteAthlete } from '../services/api';

function AthleteManagement() {
  const [athletes, setAthletes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
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
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '2rem' }}>
        <h2>Athlete Management</h2>
        <button onClick={() => setShowForm(!showForm)} className="btn-primary">
          {showForm ? 'Cancel' : '+ Add Athlete'}
        </button>
      </div>

      {error && <div className="error">{error}</div>}

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

      <div className="card">
        <h3 className="card-header">Athletes ({athletes.length})</h3>
        {athletes.length === 0 ? (
          <p style={{ textAlign: 'center', padding: '2rem', color: '#95a5a6' }}>
            No athletes yet. Click "Add Athlete" to get started.
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
