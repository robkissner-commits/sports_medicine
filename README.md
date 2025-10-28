# Sports Medicine - Injury Prevention System

A comprehensive web application for coaches to analyze athlete training data, recovery treatments, and lifestyle factors to generate personalized injury prevention plans.

## 🚀 Quick Start (One Click!)

**The easiest way to get started:**

1. **Install Prerequisites** (one time only):
   - Python 3.9+ from https://python.org (check "Add to PATH")
   - Node.js LTS from https://nodejs.org

2. **Download** the project from GitHub

3. **Double-click** `RUN_APP.bat`

4. **Wait** 5-8 minutes on first run (installs dependencies automatically)

5. **Done!** Browser opens automatically to http://127.0.0.1:3000

**Subsequent runs take only 15-20 seconds!**

See [ONE_CLICK_GUIDE.md](ONE_CLICK_GUIDE.md) for detailed instructions.

---

## Features

### Data Management
- Upload and parse CSV files from Kinexon (player tracking metrics)
- Upload and parse ATS reports (injury history, treatment logs)
- Form-based input for lifestyle data (sleep, nutrition, stress, hydration)
- Complete athlete profile management with historical tracking

### Analytics & Risk Assessment
- **ACWR Calculation**: Acute:Chronic Workload Ratio for each athlete
- **Training Load Tracking**: Cumulative training loads over time
- **Composite Risk Scores** based on:
  - Training load trends and spikes
  - Recovery treatment frequency
  - Sleep and lifestyle factors
  - Historical injury patterns
- Real-time risk level identification (Low/Medium/High)

### Visualization Dashboard
- **Team Overview**: All athletes with color-coded risk indicators
- **Individual Athlete Profiles** with:
  - Interactive ACWR trend charts (8 weeks)
  - Training load history with bar charts
  - Risk score breakdown and history
  - Lifestyle metrics trends
- Filter by date ranges and risk levels

### Personalized Recommendations
- Automated alerts when athletes exceed risk thresholds
- Specific intervention recommendations:
  - Training volume/intensity adjustments
  - Recovery modality suggestions
  - Lifestyle factor improvements
- Exportable prevention plans

---

## Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: Database ORM
- **SQLite/PostgreSQL**: Database (SQLite for development, easily switchable to PostgreSQL)
- **Pandas**: CSV parsing and data analysis
- **NumPy**: Scientific computing for risk calculations

### Frontend
- **React 18**: UI framework
- **Vite**: Build tool and dev server
- **Recharts**: Interactive data visualizations
- **Axios**: HTTP client
- **React Router**: Navigation

---

## Project Structure

```
sports_medicine/
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database setup and session management
│   ├── models.py            # SQLAlchemy database models
│   ├── schemas.py           # Pydantic validation schemas
│   ├── analytics.py         # Risk calculation and ACWR algorithms
│   └── routers/
│       ├── athletes.py      # Athlete management endpoints
│       ├── data_upload.py   # CSV upload and parsing
│       ├── lifestyle.py     # Lifestyle logging endpoints
│       └── dashboard.py     # Analytics and dashboard endpoints
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   ├── services/
│   │   │   └── api.js       # API client
│   │   └── pages/
│   │       ├── TeamDashboard.jsx      # Team overview page
│   │       ├── AthleteDetail.jsx      # Individual athlete page
│   │       ├── AthleteManagement.jsx  # Athlete CRUD
│   │       ├── DataUpload.jsx         # File upload interface
│   │       └── ConnectionTest.jsx     # Diagnostics page
│   ├── package.json
│   └── vite.config.js
├── sample_data/             # Sample CSV files for testing
├── requirements.txt         # Python dependencies
├── RUN_APP.bat             # ⭐ ONE-CLICK LAUNCHER
├── FIX_BACKEND.bat         # Fix backend dependencies
├── FIX_FRONTEND.bat        # Fix frontend dependencies
├── STOP_APP.bat            # Stop all servers
├── TROUBLESHOOT.bat        # Network diagnostics
├── README.md               # This file
├── ONE_CLICK_GUIDE.md      # How to use RUN_APP.bat
└── TROUBLESHOOTING_GUIDE.md # Comprehensive troubleshooting
```

---

## Launcher Scripts

| Script | Purpose | When to Use |
|--------|---------|-------------|
| **RUN_APP.bat** ⭐ | Main launcher - does everything automatically | **Use this!** Start the app |
| FIX_BACKEND.bat | Reinstall Python dependencies | If backend has errors |
| FIX_FRONTEND.bat | Reinstall Node.js dependencies | If frontend has errors |
| STOP_APP.bat | Stop both servers | When done using the app |
| TROUBLESHOOT.bat | Test network connections | If getting connection errors |

**Recommendation:** Just use `RUN_APP.bat` for everything!

---

## Usage Guide

### 1. Add Athletes

Navigate to "Manage Athletes" and click "Add Athlete":
- Enter athlete name (required)
- Add optional information: position, age, email, team
- Submit to create the athlete profile

### 2. Upload Training Data

Go to "Upload Data" page:

**Training Loads (Kinexon)**:
- Select "Training Loads" as upload type
- Choose an athlete or select "Auto-detect" for bulk upload
- Upload CSV with columns:
  - `date` (YYYY-MM-DD)
  - `training_load` or `load`
  - `athlete_name` or `athlete_id`
  - Optional: `total_distance`, `high_speed_distance`, `accelerations`, etc.

**Treatments (ATS)**:
- Select "Treatments" as upload type
- Upload CSV with:
  - `date`, `modality`, `athlete_name`
  - Optional: `duration`, `body_part`, `severity`, `notes`

**Injury History**:
- Select "Injury History"
- Upload CSV with:
  - `injury_date`, `injury_type`, `body_part`, `athlete_name`
  - Optional: `severity`, `recovery_date`, `days_missed`

### 3. Calculate Risk Assessments

**For all athletes**:
- Go to Team Dashboard
- Click "Recalculate All Risks"

**For individual athlete**:
- Click on athlete in Team Dashboard
- Click "Recalculate Risk" on their profile page

### 4. View Analytics

**Team Dashboard**:
- View all athletes with color-coded risk levels
- See summary statistics (total athletes, risk distribution)
- Filter by risk level (High/Medium/Low)
- Click on any athlete to see detailed analysis

**Athlete Detail Page**:
- View current risk status and ACWR
- Interactive ACWR trend chart (8 weeks)
- Training load bar chart (28 days)
- Risk assessment history
- Personalized recommendations

**Connection Test Page**:
- Navigate to "Connection Test" tab
- See real-time diagnostics of backend/frontend connection
- Troubleshoot network issues

---

## Risk Calculation Methodology

### ACWR (Acute:Chronic Workload Ratio)
```
ACWR = Acute Load (7-day average) / Chronic Load (28-day rolling average)
```

**Risk Thresholds**:
- High Risk: ACWR > 1.5 or < 0.8
- Moderate Risk: ACWR > 1.3 or < 0.9
- Low Risk: 0.9 ≤ ACWR ≤ 1.3

### Overall Risk Score (0-100)
Weighted combination of:
- ACWR Risk (30%)
- Load Spike Score (25%)
- Recovery Score (20%)
- Lifestyle Score (15%)
- Injury History Score (10%)

**Risk Levels**:
- High: Score ≥ 70
- Medium: Score ≥ 40
- Low: Score < 40

---

## Sample Data

Sample CSV files are provided in `sample_data/`:
- `sample_athletes.csv` - 5 example athletes
- `sample_training_loads.csv` - 28 days of training data
- `sample_treatments.csv` - Recovery treatment records
- `sample_injuries.csv` - Injury history examples

To test the system:
1. Start the app with `RUN_APP.bat`
2. Go to "Manage Athletes" and create athletes from sample_athletes.csv
3. Upload sample_training_loads.csv via "Upload Data"
4. Upload sample_treatments.csv and sample_injuries.csv
5. Click "Recalculate All Risks" on Team Dashboard
6. Explore individual athlete profiles

---

## API Endpoints

### Athletes
- `GET /athletes/` - List all athletes
- `POST /athletes/` - Create new athlete
- `GET /athletes/{id}` - Get athlete details
- `PUT /athletes/{id}` - Update athlete
- `DELETE /athletes/{id}` - Delete athlete
- `POST /athletes/{id}/calculate-risk` - Calculate risk for athlete

### Data Upload
- `POST /upload/training-loads` - Upload Kinexon CSV
- `POST /upload/treatments` - Upload ATS treatment CSV
- `POST /upload/injuries` - Upload injury history CSV

### Dashboard
- `GET /dashboard/team-overview` - Team overview with risk levels
- `POST /dashboard/calculate-all-risks` - Calculate risk for all athletes
- `GET /dashboard/athlete/{id}/acwr-trend` - ACWR trend data
- `GET /dashboard/athlete/{id}/training-summary` - Training statistics

### Lifestyle
- `POST /lifestyle/` - Create lifestyle log
- `GET /lifestyle/athlete/{id}` - Get athlete lifestyle logs

Full API documentation: `http://127.0.0.1:8000/docs`

---

## Troubleshooting

### Application Won't Start

**Check Prerequisites:**
- Python 3.9+ installed: `python --version`
- Node.js installed: `node --version`
- Both should return version numbers

**If "Module not found" errors:**
1. Close all windows
2. Run `FIX_BACKEND.bat`
3. Run `FIX_FRONTEND.bat`
4. Run `RUN_APP.bat` again

**If "Port already in use":**
1. Run `STOP_APP.bat`
2. Wait 5 seconds
3. Run `RUN_APP.bat` again

### Network Errors

**If seeing "Failed to load" errors:**
1. Click "Connection Test" in navigation
2. Check which tests fail (red X)
3. See [TROUBLESHOOTING_GUIDE.md](TROUBLESHOOTING_GUIDE.md) for detailed help

**Quick fix:**
1. Close both terminal windows
2. Run `STOP_APP.bat`
3. Run `RUN_APP.bat` again

### Common Issues

**Backend shows "uvicorn not found":**
- Run `FIX_BACKEND.bat`

**Frontend shows "module not found":**
- Run `FIX_FRONTEND.bat`

**"Python is not recognized":**
- Install Python from python.org
- Check "Add to PATH" during installation
- Restart computer

**"npm is not recognized":**
- Install Node.js from nodejs.org
- Restart computer

For comprehensive troubleshooting, see [TROUBLESHOOTING_GUIDE.md](TROUBLESHOOTING_GUIDE.md)

---

## Configuration

### Environment Variables
Create a `.env` file with:

```env
DATABASE_URL=sqlite:///./sports_medicine.db
API_HOST=127.0.0.1
API_PORT=8000
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

For PostgreSQL:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/sports_medicine
```

---

## Development

### Manual Start (Advanced)

If you prefer manual control:

**Backend:**
```bash
cd /path/to/sports_medicine
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python run_backend.py
```

**Frontend (new terminal):**
```bash
cd /path/to/sports_medicine/frontend
npm install
npm run dev
```

### Building for Production

**Backend:**
```bash
pip install gunicorn
gunicorn backend.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**Frontend:**
```bash
cd frontend
npm run build
# Serve the 'dist' folder with any static file server
```

---

## Future Enhancements (Phase 2)

- [ ] API integration for automated Kinexon data imports
- [ ] Email/SMS alerts for high-risk athletes
- [ ] Comparison tools (athlete vs team average)
- [ ] Custom threshold settings per athlete
- [ ] Machine learning predictions for injury risk
- [ ] PDF report generation
- [ ] Multi-team management
- [ ] User authentication and authorization
- [ ] Mobile app

---

## Support

Having issues? Check these resources:

1. **[ONE_CLICK_GUIDE.md](ONE_CLICK_GUIDE.md)** - How to use RUN_APP.bat
2. **[TROUBLESHOOTING_GUIDE.md](TROUBLESHOOTING_GUIDE.md)** - Comprehensive troubleshooting (10+ solutions)
3. **Connection Test Page** - http://127.0.0.1:3000/test (real-time diagnostics)
4. **API Docs** - http://127.0.0.1:8000/docs (interactive API documentation)

---

## License

This project is provided as-is for educational and professional use in sports medicine and athletic training.

---

## Summary

**To get started in 3 steps:**
1. Install Python and Node.js
2. Double-click `RUN_APP.bat`
3. Start analyzing athlete data!

Everything else is automatic! 🚀
