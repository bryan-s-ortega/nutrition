# Manage project commands

# Kill processes on ports 8000 (Backend) and 8081 (Frontend)
kill-ports:
    @echo "Stopping Backend (Port 8000)..."
    -fuser -k 8000/tcp
    @echo "Stopping Frontend (Port 8081)..."
    -fuser -k 8081/tcp
    @echo "Stopping Database Proxy (Port 5432)..."
    -fuser -k 5432/tcp
    @echo "Ports cleared."

# Run the Backend (FastAPI) with Cloud SQL Proxy
backend:
    npx concurrently -k -n "PROXY,API" -c "blue,green" "just db-proxy" "just _backend-run"

# Internal: Run Uvicorn directly (Waits for DB)
_backend-run:
    @echo "Waiting for Database Proxy to be ready..."
    @bash -c 'for i in {1..30}; do if (echo > /dev/tcp/127.0.0.1/5432) >/dev/null 2>&1; then break; fi; sleep 1; done'
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

# Start Cloud SQL Proxy (Requires Terraform output)
db-proxy:
    @echo "Fetching connection name from Terraform..."
    cloud-sql-proxy `cd terraform && terraform output -raw database_connection_name`
