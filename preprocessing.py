import os
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download NLTK stopwords
nltk.download('stopwords')
nltk.download('punkt')

# Function to clean text
def clean_text(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    text = re.sub(r'\d+', '', text)  # Remove numbers
    text = re.sub(r'[^\w\s]', '', text)  # Remove special characters and punctuation
    
    # Tokenize and remove stopwords
    words = word_tokenize(text)
    words = [word for word in words if word not in stopwords.words('english')]
    
    return ' '.join(words)

# Function to preprocess files in a directory
def preprocess_files(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)

        # Read text file
        with open(input_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # Clean text
        cleaned_text = clean_text(text)

        # Save preprocessed text
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(cleaned_text)

        print(f"Processed {filename} and saved to {output_path}")

# Define directories
resumes_input_dir = "extracted_text/resumes"
job_desc_input_dir = "extracted_text/job_descriptions"
resumes_output_dir = "preprocessed_text/resumes"
job_desc_output_dir = "preprocessed_text/job_descriptions"

# Process resumes and job descriptions
preprocess_files(resumes_input_dir, resumes_output_dir)
preprocess_files(job_desc_input_dir, job_desc_output_dir)

print("✅ Preprocessing completed for both resumes and job descriptions.")
