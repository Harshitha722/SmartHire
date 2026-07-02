import pandas as pd
import numpy as np
import os
import joblib
from sklearn.metrics.pairwise import cosine_similarity
from app.ml.train_model import clean_text

def get_job_recommendations(resume_text, top_n=10):
    # Load Vectorizer
    trained_models_dir = os.path.join(os.path.dirname(__file__), "../../../trained_models")
    vectorizer_path = os.path.join(trained_models_dir, "tfidf_vectorizer.pkl")
    
    if not os.path.exists(vectorizer_path):
        return []
        
    tfidf = joblib.load(vectorizer_path)
    
    # Load Jobs Dataset
    dataset_path = os.path.join(os.path.dirname(__file__), "../../../dataset/jobs_dataset.csv")
    if not os.path.exists(dataset_path):
        return []
        
    jobs_df = pd.read_csv(dataset_path)
    
    # Combine required skills and description for the job text
    jobs_df['job_text'] = jobs_df['requiredSkills'] + " " + jobs_df['description']
    jobs_df['cleaned_job_text'] = jobs_df['job_text'].apply(clean_text)
    
    # Vectorize
    job_vectors = tfidf.transform(jobs_df['cleaned_job_text'])
    
    # Clean and Vectorize Resume
    cleaned_resume = clean_text(resume_text)
    resume_vector = tfidf.transform([cleaned_resume])
    
    # Calculate Cosine Similarity
    similarities = cosine_similarity(resume_vector, job_vectors).flatten()
    
    # Get top N jobs
    top_indices = similarities.argsort()[-top_n:][::-1]
    
    recommendations = []
    for idx in top_indices:
        match_score = float(similarities[idx] * 100)
        job_data = jobs_df.iloc[idx]
        recommendations.append({
            "jobId": str(job_data['id']),
            "title": str(job_data['title']),
            "company": str(job_data['company']),
            "location": str(job_data['location']),
            "salary": str(job_data['salary']),
            "matchPercentage": round(match_score, 2),
            "requiredSkills": eval(job_data['requiredSkills']) if isinstance(job_data['requiredSkills'], str) else job_data['requiredSkills']
        })
        
    return recommendations
