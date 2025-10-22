# Sports Medicine - Injury Prevention System

A comprehensive web application for coaches to analyze athlete training data, recovery treatments, and lifestyle factors to generate personalized injury prevention plans.

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
│   │       └── DataUpload.jsx         # File upload interface
│   ├── package.json
│   └── vite.config.js
├── sample_data/             # Sample CSV files for testing
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Installation & Setup

### Prerequisites
- Python 3.9+
- Node.js 18+
- npm or yarn

### Backend Setup

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Create environment file (optional):
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Initialize the database and start the server:
```bash
python run_backend.py
```

The API will be available at `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

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

## Sample Data

Sample CSV files are provided in `sample_data/`:
- `sample_athletes.csv` - 5 example athletes
- `sample_training_loads.csv` - 28 days of training data
- `sample_treatments.csv` - Recovery treatment records
- `sample_injuries.csv` - Injury history examples

To test the system:
1. Start both backend and frontend
2. Go to "Manage Athletes" and create athletes from sample_athletes.csv
3. Upload sample_training_loads.csv via "Upload Data"
4. Upload sample_treatments.csv and sample_injuries.csv
5. Click "Recalculate All Risks" on Team Dashboard
6. Explore individual athlete profiles

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

Full API documentation: `http://localhost:8000/docs`

## Database Schema

### Tables
- **athletes** - Athlete profiles
- **training_loads** - Daily training metrics
- **treatments** - Recovery treatments
- **lifestyle_logs** - Daily lifestyle metrics
- **risk_assessments** - Calculated risk scores
- **injury_history** - Historical injuries

## Configuration

### Environment Variables
Create a `.env` file with:

```env
DATABASE_URL=sqlite:///./sports_medicine.db
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

For PostgreSQL:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/sports_medicine
```

## Development

### Running Tests
```bash
# Backend tests (if implemented)
pytest

# Frontend tests
cd frontend
npm test
```

### Building for Production

**Backend**:
```bash
# Install production server
pip install gunicorn

# Run with gunicorn
gunicorn backend.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**Frontend**:
```bash
cd frontend
npm run build
# Serve the 'dist' folder with any static file server
```

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

## Troubleshooting

**Backend won't start**:
- Check if port 8000 is available
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check database permissions

**Frontend won't start**:
- Delete `node_modules` and run `npm install` again
- Check if port 3000 is available
- Verify backend is running

**CSV upload fails**:
- Check file format (CSV or Excel)
- Verify column names match expected format
- Ensure athlete exists if specifying athlete_id
- Check backend logs for detailed error messages

**No data showing**:
- Ensure you've uploaded training data
- Click "Recalculate All Risks" after uploading data
- Check that athletes have at least 7 days of training data for ACWR

## Support

For issues, questions, or feature requests, please create an issue in the repository.

## License

This project is provided as-is for educational and professional use in sports medicine and athletic training.
