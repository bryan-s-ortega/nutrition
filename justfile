# Manage project commands

# Kill processes on ports 8000 (Backend) and 8081 (Frontend)
kill-ports:
    @echo "Stopping Backend (Port 8000)..."
    -fuser -k 8000/tcp
    @echo "Stopping Frontend (Port 8081)..."
    -fuser -k 8081/tcp
    @echo "Ports cleared."

# Run the Backend (FastAPI)
backend:
    cd backend && uv run uvicorn main:app --reload

# Run the Mobile App (Web)
mobile-web:
    cd mobile && npm run web

# Run Backend Tests
test:
    uv run pytest backend/tests
