import joblib
import os
import re
import nltk
import string
import sys
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the trained model and vectorizer
model = joblib.load("job_matching_model.joblib")
vectorizer = joblib.load("vectorizer.joblib")

# Function to preprocess text
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)  # Remove numbers
    text = text.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
    text = ' '.join(text.split())  # Remove extra spaces
    return text

# Function to test model on new text
def predict_label(text):
    text = preprocess_text(text)
    text_vectorized = vectorizer.transform([text])  # Transform text
    prediction = model.predict(text_vectorized)  # Predict
    return prediction[0]

# Take input file from command line
if len(sys.argv) < 2:
    print("Usage: python test_model.py <file_path>")
    sys.exit(1)

file_path = sys.argv[1]

if not os.path.exists(file_path):
    print("Error: File does not exist.")
    sys.exit(1)

# Read the input file
with open(file_path, "r", encoding="utf-8") as file:
    text = file.read()

# Predict the label (Resume or Job Description)
predicted_label = predict_label(text)
print(f"Predicted Label: {predicted_label}")
