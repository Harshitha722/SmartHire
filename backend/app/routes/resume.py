from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.services.resume_parser import extract_text_from_file
import shutil
import os
import uuid
from datetime import datetime
from app.database.connection import get_database

router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "../../uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    # Validate extension
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ['.pdf', '.docx']:
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are allowed.")
        
    # Save file temporarily
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}{ext}")
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Parse text
    parsed_text = extract_text_from_file(file_path)
    if not parsed_text:
        raise HTTPException(status_code=400, detail="Could not extract text from the file.")
        
    # Store in database
    db = get_database()
    resumes_collection = db["resumes"]
    
    resume_doc = {
        "id": file_id,
        "filename": file.filename,
        "filePath": file_path,
        "parsedText": parsed_text,
        "createdAt": datetime.utcnow()
    }
    
    await resumes_collection.insert_one(resume_doc)
    
    return {"message": "Resume uploaded successfully", "resumeId": file_id, "parsed_text_preview": parsed_text[:200] + "..."}
