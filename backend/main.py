from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

# Allow running either as a package (e.g. `uvicorn backend.main:app`)
# or as a module/script from this directory (e.g. `uvicorn main:app`).
try:
    from .database import create_db_and_tables
    from .routes import onboarding, food
except ImportError:  # pragma: no cover
    from database import create_db_and_tables
    from routes import onboarding, food


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title="Nutrition App Backend", lifespan=lifespan)

# Add CORS Middleware to allow requests from Frontend (Web/Mobile)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, allow all. In prod, specify domains.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(onboarding.router)
app.include_router(food.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Nutrition App API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
