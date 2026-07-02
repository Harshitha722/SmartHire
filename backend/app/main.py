from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager

from app.database.connection import check_db_connection
from app.routes import auth, resume, ml, recruiter

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    await check_db_connection()
    yield
    # Shutdown actions
    pass

app = FastAPI(
    title="SmartHire AI API",
    description="Backend API for SmartHire AI - Resume Screening & Job Recommendation Platform",
    version="1.0.0",
    lifespan=lifespan
)

# Allow CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, this should be restricted
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(resume.router)
app.include_router(ml.router)
app.include_router(recruiter.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to SmartHire AI API!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
