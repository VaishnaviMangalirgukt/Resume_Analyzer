from sklearn.feature_extraction.text import TfidfVectorizer
import os
import joblib  # Import joblib for saving the vectorized data

# Read preprocessed text
def load_data(input_dir):
    texts = []
    filenames = []
    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            texts.append(file.read())
            filenames.append(filename)
    return texts, filenames

# Example TF-IDF vectorization
def vectorize_data(texts):
    vectorizer = TfidfVectorizer(max_features=5000)
    X = vectorizer.fit_transform(texts)
    return X

# Example usage
input_dir = 'processed_text'  # Your directory with preprocessed text files
texts, filenames = load_data(input_dir)
X = vectorize_data(texts)

# Save the vectorized data to a file
joblib.dump(X, 'vectorized_data.pkl')  # Save the vectorized data

print(f"Vectorized data shape: {X.shape}")
print("Vectorized data has been saved to 'vectorized_data.pkl'")
