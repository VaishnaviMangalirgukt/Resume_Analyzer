import pandas as pd
import joblib

# Load the vectorized data (X_tfidf) from the saved file (if saved in joblib format)
X_tfidf = joblib.load('vectorized_data.pkl')  # Adjust the path if needed

# Convert the sparse matrix to a dense matrix (2D numpy array)
dense_matrix = X_tfidf.toarray()

# Create a Pandas DataFrame from the dense matrix
df = pd.DataFrame(dense_matrix)

# Save the DataFrame as a CSV file
df.to_csv('vectorized_data.csv', index=False)

print("Vectorized data has been saved to vectorized_data.csv")
