from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.database.connection import get_database
import uuid

router = APIRouter(
    prefix="/recruiter",
    tags=["Recruiter"]
)

class JobCreate(BaseModel):
    title: str
    description: str
    required_skills: List[str]

@router.post("/job")
async def create_job(job: JobCreate):
    db = get_database()
    job_id = str(uuid.uuid4())
    
    new_job = {
        "id": job_id,
        "title": job.title,
        "description": job.description,
        "requiredSkills": job.required_skills
    }
    
    await db["jobs"].insert_one(new_job)
    return {"message": "Job created successfully", "jobId": job_id}

@router.get("/candidates")
async def get_candidates():
    db = get_database()
    cursor = db["resumes"].find({}, {"parsedText": 0}) # Exclude large text for list view
    candidates = await cursor.to_list(length=100)
    
    # Format for JSON serialization (convert ObjectId to string if needed, though we use custom string IDs)
    for c in candidates:
        if "_id" in c:
            c["_id"] = str(c["_id"])
            
    return {"candidates": candidates}
