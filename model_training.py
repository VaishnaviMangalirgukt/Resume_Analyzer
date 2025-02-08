import joblib
import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfVectorizer

# Step 1: Load the vectorized data and labels
def load_data():
    # Load vectorized data (Assuming it's saved as 'vectorized_data.pkl')
    X_tfidf = joblib.load('vectorized_data.pkl')

    # Load labels (Assuming labels are stored in a text file with each label on a new line)
    labels = []
    with open('labels.txt', 'r') as file:
        for line in file:
            labels.append(line.strip())  # Assuming labels are stored in a file, one per line

    return X_tfidf, labels

# Step 2: Check data consistency
def check_data_consistency():
    processed_resumes = len(os.listdir("processed_text"))
    label_count = len(open("labels.txt").readlines())

    print(f"Processed resumes count: {processed_resumes}")
    print(f"Labels count: {label_count}")

    if processed_resumes != label_count:
        raise ValueError("Mismatch between processed resumes and labels. Please check your data!")

# Step 3: Train the classifier
def train_classifier(X, labels):
    X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.3, random_state=42)

    # Train a Logistic Regression classifier
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    # Evaluate the model
    evaluate_model(model, X_test, y_test)

    return model

# Step 4: Evaluate the model
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    print(f"\nClassification Report:\n{classification_report(y_test, y_pred)}")

# Step 5: Save the trained model
def save_model(model):
    joblib.dump(model, 'resume_classifier_model.pkl')  # Save the trained model
    print("Model saved successfully!")

def main():
    check_data_consistency()  # Ensure labels and resumes match
    X, labels = load_data()  # Load vectorized data and labels
    model = train_classifier(X, labels)  # Train classifier
    save_model(model)  # Save the trained model

if __name__ == "__main__":
    main()
