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

# Lint and Format Check (Ruff)
lint:
    cd backend && uv run ruff check .
    cd backend && uv run ruff format --check .

# Run Backend Tests
test:
    cd backend && PYTHONPATH=. uv run pytest

# Destroy Infrastructure (Use with CAUTION)
destroy:
    cd terraform && terraform destroy -auto-approve
    @echo "Infrastructure destroyed. Trigger the GitHub Action to recreate."
