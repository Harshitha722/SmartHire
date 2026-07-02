import os
from PyPDF2 import PdfReader
import docx

def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    if ext == '.pdf':
        try:
            reader = PdfReader(file_path)
            for page in reader.pages:
                text += page.extract_text() + " "
        except Exception as e:
            print(f"Error reading PDF: {e}")
    elif ext == '.docx':
        try:
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text += para.text + " "
        except Exception as e:
            print(f"Error reading DOCX: {e}")
    return text.strip()

def calculate_resume_score(resume_text, required_skills):
    # Dummy logic for resume score
    # Out of 100 based on presence of keywords and length
    score = 50 # Base score
    text_lower = resume_text.lower()
    
    # Increase score based on required skills matched
    matched_skills = [skill for skill in required_skills if skill.lower() in text_lower]
    if required_skills:
        skill_score = (len(matched_skills) / len(required_skills)) * 30
        score += skill_score
        
    # Increase score based on length
    if len(resume_text) > 500:
        score += 10
    if len(resume_text) > 1000:
        score += 10
        
    return min(int(score), 100)

def extract_skills(resume_text, all_possible_skills):
    text_lower = resume_text.lower()
    extracted = []
    for skill in all_possible_skills:
        if skill.lower() in text_lower:
            extracted.append(skill)
    return extracted
