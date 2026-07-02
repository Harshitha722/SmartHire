from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import joblib
import os
from app.ml.train_model import clean_text
from app.ml.recommender import get_job_recommendations
from app.services.resume_parser import calculate_resume_score, extract_skills
from app.database.connection import get_database

router = APIRouter(
    prefix="/ml",
    tags=["Machine Learning"]
)

class ResumeRequest(BaseModel):
    resume_id: str

class SkillGapRequest(BaseModel):
    resume_id: str
    job_id: str

@router.post("/predict-role")
async def predict_role(request: ResumeRequest):
    # Fetch resume from DB
    db = get_database()
    resume_doc = await db["resumes"].find_one({"id": request.resume_id})
    if not resume_doc:
        raise HTTPException(status_code=404, detail="Resume not found")
        
    text = resume_doc["parsedText"]
    cleaned = clean_text(text)
    
    # Load Models
    trained_models_dir = os.path.join(os.path.dirname(__file__), "../../../trained_models")
    try:
        tfidf = joblib.load(os.path.join(trained_models_dir, "tfidf_vectorizer.pkl"))
        classifier = joblib.load(os.path.join(trained_models_dir, "resume_classifier.pkl"))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Models not found. Train the models first.")
        
    # Predict
    vector = tfidf.transform([cleaned])
    prediction = classifier.predict(vector)[0]
    
    # You can also get probabilities if the model supports it
    try:
        probs = classifier.predict_proba(vector)[0]
        confidence = float(max(probs) * 100)
    except:
        confidence = 100.0 # Fallback for models like LinearSVC without proba
        
    # Update DB
    await db["resumes"].update_one(
        {"id": request.resume_id},
        {"$set": {"predictedRole": prediction, "predictionConfidence": confidence}}
    )
    
    return {"predicted_role": prediction, "confidence": round(confidence, 2)}

@router.post("/recommend-jobs")
async def recommend_jobs(request: ResumeRequest):
    db = get_database()
    resume_doc = await db["resumes"].find_one({"id": request.resume_id})
    if not resume_doc:
        raise HTTPException(status_code=404, detail="Resume not found")
        
    text = resume_doc["parsedText"]
    recommendations = get_job_recommendations(text, top_n=5)
    
    return {"recommendations": recommendations}

@router.post("/resume-score")
async def resume_score(request: ResumeRequest):
    db = get_database()
    resume_doc = await db["resumes"].find_one({"id": request.resume_id})
    if not resume_doc:
        raise HTTPException(status_code=404, detail="Resume not found")
        
    # Dummy required skills for the role (In a real app, this would come from a selected Job Description)
    role = resume_doc.get("predictedRole", "Software Engineer")
    dummy_required_skills = ["Python", "SQL", "JavaScript", "React", "Docker", "AWS", "Git"]
    
    score = calculate_resume_score(resume_doc["parsedText"], dummy_required_skills)
    
    # Update DB
    await db["resumes"].update_one(
        {"id": request.resume_id},
        {"$set": {"resumeScore": score}}
    )
    
    return {"score": score}

@router.post("/skill-gap")
async def skill_gap(request: SkillGapRequest):
    db = get_database()
    resume_doc = await db["resumes"].find_one({"id": request.resume_id})
    if not resume_doc:
        raise HTTPException(status_code=404, detail="Resume not found")
        
    # In a real app, you would fetch the job from the DB to get its requiredSkills
    # For demo, using dummy required skills
    job_required_skills = ["React", "Node.js", "MongoDB", "Express", "Docker"]
    
    user_skills = extract_skills(resume_doc["parsedText"], job_required_skills + ["Python", "SQL", "Java"])
    
    missing_skills = [skill for skill in job_required_skills if skill not in user_skills]
    
    return {
        "existing_skills": user_skills,
        "missing_skills": missing_skills,
        "suggestions": [f"Learn {skill}" for skill in missing_skills]
    }
