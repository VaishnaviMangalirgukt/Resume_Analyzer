import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Function to read text from a file
def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return ""

# Function for keyword matching between resumes and job descriptions
def keyword_matching(resumes_folder, job_desc_folder, output_folder, threshold=0.5):
    # Initialize the TF-IDF vectorizer
    vectorizer = TfidfVectorizer(stop_words='english')

    # Read job descriptions
    job_desc_files = [f for f in os.listdir(job_desc_folder) if f.endswith('.txt')]
    job_descriptions = []
    for job_file in job_desc_files:
        job_path = os.path.join(job_desc_folder, job_file)
        job_descriptions.append(read_file(job_path))

    # Process resumes
    resume_files = [f for f in os.listdir(resumes_folder) if f.endswith('.txt')]
    resumes = []
    for resume_file in resume_files:
        resume_path = os.path.join(resumes_folder, resume_file)
        resumes.append(read_file(resume_path))

    # Combine job descriptions and resumes for TF-IDF fitting
    all_texts = job_descriptions + resumes
    vectorizer.fit(all_texts)

    # Calculate cosine similarity between each resume and job description
    for job_idx, job_desc in enumerate(job_descriptions):
        job_desc_vec = vectorizer.transform([job_desc])
        
        for resume_idx, resume in enumerate(resumes):
            resume_vec = vectorizer.transform([resume])
            similarity_score = cosine_similarity(job_desc_vec, resume_vec)[0][0]
            
            # Save result in a file if similarity score is greater than threshold
            result_file = os.path.join(output_folder, f'{resume_files[resume_idx]}_vs_{job_desc_files[job_idx]}_match.txt')
            with open(result_file, 'w', encoding='utf-8') as f:
                f.write(f"Job Description: {job_desc_files[job_idx]}\n")
                f.write(f"Resume: {resume_files[resume_idx]}\n")
                f.write(f"Similarity Score: {similarity_score:.4f}\n")
                f.write(f"Keywords Matched: {similarity_score > threshold}\n")  # If similarity score is greater than threshold, it's a match
            print(f"Processed {resume_files[resume_idx]} and saved match results.")

# Main function to run the matching
if __name__ == "__main__":
    resumes_folder = 'extracted_text/resumes'  # Folder containing resume text files
    job_desc_folder = 'job_descriptions'      # Folder containing job description text files
    output_folder = 'categorized_output'      # Folder to save match results
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    keyword_matching(resumes_folder, job_desc_folder, output_folder, threshold=0.5)
