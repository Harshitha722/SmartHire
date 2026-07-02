# SmartHire AI 

> AI-powered Resume Screening, Skill Gap Analysis, and Job Recommendation Platform.

SmartHire AI is a modern SaaS platform designed to bridge the gap between candidates and recruiters using advanced Machine Learning and NLP. 
It analyzes resumes to extract skills, predict suitable job roles, score the resume against ATS standards, and recommend the best-matching job openings.

## 🌟 Features

### 👤 Candidate Workspace
- **Resume Parsing:** Upload PDF/DOCX resumes and automatically extract skills, text, and structure.
- **AI Job Role Prediction:** Uses an NLP classification model to predict the most suitable tech role (e.g., Software Engineer, Data Scientist).
- **Resume Scoring:** Generates an ATS-style score out of 100 based on keyword density and content.
- **Skill Gap Analysis:** Highlights existing skills, missing skills, and suggests areas for improvement.
- **Job Recommendations:** Suggests the Top 10 matching jobs using TF-IDF and Cosine Similarity.

### 🏢 Recruiter Workspace
- **Job Posting:** Upload Job Descriptions to automatically build matching profiles.
- **Candidate Ranking:** View a centralized dashboard of all applicants ranked by their AI match score.

## 🏗️ Tech Stack

<div align="left">
  
  **Frontend** <br>
  <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" />
  <img src="https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white" />
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" />
  <img src="https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white" />

  <br><br>
  **Backend** <br>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Uvicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white" />

  <br><br>
  **Machine Learning & Data Science** <br>
  <img src="https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" />
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" />
  <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" />
  <img src="https://img.shields.io/badge/spaCy-09A3D5?style=for-the-badge&logo=spacy&logoColor=white" />

  <br><br>
  **Database** <br>
  <img src="https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white" />
  
</div>

## 📂 Folder Structure
```
smarthire/
├── frontend/             # React Vite Application
│   ├── src/
│   │   ├── components/   # Reusable UI components
│   │   ├── pages/        # Views (Home, Candidate, Recruiter)
│   │   ├── index.css     # Global styles & design tokens
│   │   └── App.jsx       # Routing setup
├── backend/              # FastAPI Application
│   ├── app/
│   │   ├── database/     # MongoDB connection
│   │   ├── ml/           # Model training and prediction logic
│   │   ├── models/       # Pydantic schemas
│   │   ├── routes/       # API endpoints (Auth, Resume, ML)
│   │   └── services/     # Core logic (PDF parsing)
│   ├── uploads/          # Temporary file storage
│   └── requirements.txt  # Python dependencies
├── dataset/              # Synthetic Mock Data
│   ├── resume_dataset.csv
│   └── jobs_dataset.csv
└── trained_models/       # Saved .pkl ML models
```

## 🧠 Machine Learning Documentation

The NLP Pipeline performs the following operations:
1. **Text Cleaning**: Converts text to lowercase, removes special characters, and digits.
2. **Stop Word Removal & Lemmatization**: Uses NLTK and spaCy to reduce words to their base form.
3. **TF-IDF Vectorization**: Transforms the text corpus into numerical vectors based on Term Frequency-Inverse Document Frequency.
4. **Classification Models Evaluated**:
   - Logistic Regression
   - Naive Bayes (MultinomialNB)
   - Linear SVM
   - Random Forest
5. **Recommendation Engine**: Uses Cosine Similarity between the candidate's TF-IDF vector and available Job Description vectors to find the highest matches.

## 🚀 Installation & Setup

### 1. Prerequisites
- Node.js (v18+)
- Python (3.10+)
- MongoDB (Running locally on port 27017 or update the connection string)

### 2. Backend Setup
```bash
# Navigate to project root
python -m venv venv
# Activate virtual environment
.\venv\Scripts\activate
pip install -r backend/requirements.txt
# Download NLP model
python -m spacy download en_core_web_sm
# Train the models (Required before starting server)
python backend/app/ml/train_model.py
# Start the FastAPI Server
uvicorn backend.app.main:app --reload
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## 🌐 API Documentation
FastAPI provides automatic interactive API documentation.
Once the backend is running, visit:
- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

## 🔮 Future Scope
- Cover Letter Generation using LLMs.
- Interview Question Generation based on missing skills.
- Email Notifications for candidates upon status updates.
