import os
import pandas as pd
from sentence_transformers import SentenceTransformer, util

# Load the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def load_text(file_path):
    """Load text content from a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def rank_resumes(job_desc_path, resume_folder, output_file, threshold=50.0):
    """Rank all resumes against a given job description and filter by similarity threshold."""
    job_desc_text = load_text(job_desc_path)
    job_desc_embedding = model.encode(job_desc_text, convert_to_tensor=True)
    
    results = []
    
    for resume_file in os.listdir(resume_folder):
        if resume_file.endswith(".txt"):
            resume_path = os.path.join(resume_folder, resume_file)
            resume_text = load_text(resume_path)
            resume_embedding = model.encode(resume_text, convert_to_tensor=True)
            
            similarity = util.pytorch_cos_sim(job_desc_embedding, resume_embedding).item() * 100
            if similarity >= threshold:
                results.append((resume_file, similarity))
    
    # Sort resumes by similarity score (descending order)
    results.sort(key=lambda x: x[1], reverse=True)
    
    # Save to CSV file
    df = pd.DataFrame(results, columns=["Resume", "Similarity (%)"])
    df.to_csv(output_file, index=False)
    print(f"✅ Ranking saved to {output_file} with resumes having similarity >= {threshold}%")

# Example usage
job_description_path = "preprocessed_text/job_descriptions/Business_Analyst.txt_text.txt"
resume_folder = "preprocessed_text/resumes"
output_csv = "ranked_resumes.csv"

rank_resumes(job_description_path, resume_folder, output_csv, threshold=50.0)
