import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Athletes
export const getAthletes = () => api.get('/athletes/');
export const getAthlete = (id) => api.get(`/athletes/${id}`);
export const createAthlete = (data) => api.post('/athletes/', data);
export const updateAthlete = (id, data) => api.put(`/athletes/${id}`, data);
export const deleteAthlete = (id) => api.delete(`/athletes/${id}`);
export const calculateAthleteRisk = (id, date = null) =>
  api.post(`/athletes/${id}/calculate-risk`, null, { params: { target_date: date } });

// Training Loads
export const getAthleteTrainingLoads = (athleteId, startDate = null, endDate = null) =>
  api.get(`/athletes/${athleteId}/training-loads`, { params: { start_date: startDate, end_date: endDate } });

// Risk History
export const getAthleteRiskHistory = (athleteId, startDate = null, endDate = null) =>
  api.get(`/athletes/${athleteId}/risk-history`, { params: { start_date: startDate, end_date: endDate } });

// Dashboard
export const getTeamOverview = (team = null, riskLevel = null) =>
  api.get('/dashboard/team-overview', { params: { team, risk_level: riskLevel } });

export const calculateAllRisks = (date = null) =>
  api.post('/dashboard/calculate-all-risks', null, { params: { target_date: date } });

export const getAthleteACWRTrend = (athleteId, days = 56) =>
  api.get(`/dashboard/athlete/${athleteId}/acwr-trend`, { params: { days } });

export const getAthleteTrainingSummary = (athleteId, days = 28) =>
  api.get(`/dashboard/athlete/${athleteId}/training-summary`, { params: { days } });

// Lifestyle
export const createLifestyleLog = (data) => api.post('/lifestyle/', data);
export const getAthleteLifestyleLogs = (athleteId, startDate = null, endDate = null) =>
  api.get(`/lifestyle/athlete/${athleteId}`, { params: { start_date: startDate, end_date: endDate } });

// File Upload
export const uploadAthletes = (file) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post('/upload/athletes', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const uploadTrainingLoads = (file, athleteId = null) => {
  const formData = new FormData();
  formData.append('file', file);
  if (athleteId) {
    formData.append('athlete_id', athleteId);
  }
  return api.post('/upload/training-loads', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const uploadTreatments = (file, athleteId = null) => {
  const formData = new FormData();
  formData.append('file', file);
  if (athleteId) {
    formData.append('athlete_id', athleteId);
  }
  return api.post('/upload/treatments', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const uploadInjuries = (file, athleteId = null) => {
  const formData = new FormData();
  formData.append('file', file);
  if (athleteId) {
    formData.append('athlete_id', athleteId);
  }
  return api.post('/upload/injuries', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export default api;
