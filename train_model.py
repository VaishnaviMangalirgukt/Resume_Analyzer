import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB  # Using Naive Bayes
from sklearn.metrics import classification_report
from sklearn.utils import resample

# 📌 Load Data
df = pd.read_csv("preprocessed_text/dataset.csv")  # Ensure dataset is correctly saved

# 📌 Check Class Distribution
print("Original Class Distribution:\n", df['label'].value_counts())

# 📌 Balance Dataset (Oversampling Resumes if Needed)
resumes = df[df['label'] == 'Resume']
job_desc = df[df['label'] == 'Job Description']

if len(resumes) < len(job_desc):
    resumes_upsampled = resample(resumes, replace=True, n_samples=len(job_desc), random_state=42)
    df = pd.concat([job_desc, resumes_upsampled])
    
print("Balanced Class Distribution:\n", df['label'].value_counts())

# 📌 Feature Extraction (TF-IDF with more features)
vectorizer = TfidfVectorizer(ngram_range=(1,1), max_features=10000)
X = vectorizer.fit_transform(df['text'])
y = df['label']

# 📌 Ensure Stratified Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# 📌 Train Model (Using Naive Bayes)
model = MultinomialNB()
model.fit(X_train, y_train)

# 📌 Evaluate Model
y_pred = model.predict(X_test)
print("\n✅ Classification Report:\n", classification_report(y_test, y_pred))

# 📌 Save Model & Vectorizer
joblib.dump(model, "job_matching_model.joblib")
joblib.dump(vectorizer, "vectorizer.joblib")

print("\n✅ Model and vectorizer saved!")
