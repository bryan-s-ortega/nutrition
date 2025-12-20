# Nutrition App

A mobile application for meal planning and nutritional tracking, compatible with Android and iOS.

## Tech Stack

- **Backend**: Python (FastAPI), SQLModel, PostgreSQL (Production) / SQLite (Dev)
- **Frontend**: React Native, Expo, Expo Router
- **Database**: Google Cloud SQL (PostgreSQL)

## Project Structure

- `backend/`: FastAPI backend service.
- `mobile/`: React Native mobile application.

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js & npm
- Repo tools (git)

### Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

### Mobile Setup
```bash
cd mobile
npm install
npx expo start
```

## Environment Variables
Copy `backend/.env.example` to `backend/.env` and configure your database URL if connecting to Cloud SQL.
