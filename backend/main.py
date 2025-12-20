from fastapi import FastAPI
from contextlib import asynccontextmanager
from backend.database import create_db_and_tables
from backend.routes import onboarding

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="Nutrition App Backend", lifespan=lifespan)

app.include_router(onboarding.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Nutrition App API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
