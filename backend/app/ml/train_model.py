import pandas as pd
import numpy as np
import os
import re
import joblib
import spacy
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Ensure NLTK data is downloaded
nltk.download('stopwords')
nltk.download('wordnet')

# Load spaCy English model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    """
    NLP Pipeline:
    - Lowercase
    - Remove special characters & numbers
    - Tokenization & Stop word removal
    - Lemmatization
    """
    if not isinstance(text, str):
        return ""
    # Lowercase
    text = text.lower()
    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Lemmatize and remove stop words
    words = text.split()
    cleaned_words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    return " ".join(cleaned_words)

def train_and_evaluate():
    print("Loading dataset...")
    dataset_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../dataset/resume_dataset.csv"))
    if not os.path.exists(dataset_path):
        print(f"Dataset not found at {dataset_path}")
        return

    df = pd.read_csv(dataset_path)
    
    print("Cleaning text data...")
    df['Cleaned_Resume'] = df['Resume'].apply(clean_text)
    
    # TF-IDF Vectorization
    print("Vectorizing text...")
    tfidf = TfidfVectorizer(max_features=5000)
    X = tfidf.fit_transform(df['Cleaned_Resume'])
    y = df['Role']
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Models to compare
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Naive Bayes": MultinomialNB(),
        "Linear SVM": LinearSVC(),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42)
    }
    
    best_model = None
    best_accuracy = 0
    best_model_name = ""
    
    print("Training models...")
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"{name} Accuracy: {accuracy * 100:.2f}%")
        
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_model = model
            best_model_name = name
            
    print(f"\nBest Model: {best_model_name} with Accuracy: {best_accuracy * 100:.2f}%")
    
    # Save the vectorizer and best model
    trained_models_dir = os.path.join(os.path.dirname(__file__), "../../../trained_models")
    os.makedirs(trained_models_dir, exist_ok=True)
    
    joblib.dump(tfidf, os.path.join(trained_models_dir, "tfidf_vectorizer.pkl"))
    joblib.dump(best_model, os.path.join(trained_models_dir, "resume_classifier.pkl"))
    print("Models saved successfully in trained_models/ directory.")

if __name__ == "__main__":
    train_and_evaluate()
