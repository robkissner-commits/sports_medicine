# Quick Start Guide

Get the Sports Medicine Injury Prevention System running in 5 minutes!

## Prerequisites

- Python 3.9+
- Node.js 18+
- npm

## Setup Steps

### 1. Install Backend Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

### 3. Start the Backend

```bash
# From the root directory
python run_backend.py
```

The backend will start at `http://localhost:8000`
- API docs available at: `http://localhost:8000/docs`

### 4. Start the Frontend (in a new terminal)

```bash
cd frontend
npm run dev
```

The frontend will start at `http://localhost:3000`

## Test with Sample Data

1. Open `http://localhost:3000` in your browser
2. Go to "Manage Athletes"
3. Add athletes manually or create them from `sample_data/sample_athletes.csv`
4. Go to "Upload Data"
5. Upload the sample files:
   - `sample_data/sample_training_loads.csv` (Training Loads)
   - `sample_data/sample_treatments.csv` (Treatments)
   - `sample_data/sample_injuries.csv` (Injury History)
6. Go to "Team Dashboard"
7. Click "Recalculate All Risks"
8. Click on any athlete to view detailed analytics

## What You'll See

- **Team Dashboard**: Overview of all athletes with risk indicators
- **Individual Athlete Pages**:
  - ACWR trends over 8 weeks
  - Training load charts
  - Risk assessment history
  - Personalized recommendations
- **Data Upload**: Easy CSV upload interface
- **Athlete Management**: Add, edit, and manage athlete profiles

## Next Steps

- Add your own athletes
- Upload your own training data
- Explore the analytics and recommendations
- Check out the full README.md for advanced features

## Troubleshooting

**Port already in use?**
- Backend: Edit `backend/config.py` to change `API_PORT`
- Frontend: Edit `frontend/vite.config.js` to change `server.port`

**Database errors?**
- Delete `sports_medicine.db` and restart the backend

**Module not found?**
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` again

**Frontend won't start?**
- Delete `frontend/node_modules`
- Run `npm install` again in the frontend directory
