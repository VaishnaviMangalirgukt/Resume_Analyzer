import os
import pandas as pd
import spacy
from sentence_transformers import SentenceTransformer, util

# Load the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')
nlp = spacy.load("en_core_web_sm")

# Predefined list of common skills (this can be expanded)
skill_keywords = {"Python", "Java", "SQL", "Machine Learning", "Data Analysis", "Project Management", "Leadership", "Communication", "Excel", "Power BI"}

def load_text(file_path):
    """Load text content from a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_skills(text):
    """Extract relevant skills from text using keyword matching."""
    words = set(word.text for word in nlp(text))
    return list(skill_keywords.intersection(words))

def rank_resumes(job_desc_path, resume_folder, output_file, threshold=50.0):
    """Rank all resumes against a given job description and extract skills."""
    job_desc_text = load_text(job_desc_path)
    job_desc_embedding = model.encode(job_desc_text, convert_to_tensor=True)
    job_skills = extract_skills(job_desc_text)
    
    results = []
    
    for resume_file in os.listdir(resume_folder):
        if resume_file.endswith(".txt"):
            resume_path = os.path.join(resume_folder, resume_file)
            resume_text = load_text(resume_path)
            resume_embedding = model.encode(resume_text, convert_to_tensor=True)
            
            similarity = util.pytorch_cos_sim(job_desc_embedding, resume_embedding).item() * 100
            resume_skills = extract_skills(resume_text)
            matching_skills = list(set(resume_skills) & set(job_skills))
            missing_skills = list(set(job_skills) - set(resume_skills))
            
            if similarity >= threshold:
                results.append((resume_file, similarity, ", ".join(resume_skills), ", ".join(matching_skills), ", ".join(missing_skills)))
    
    # Sort resumes by similarity score (descending order)
    results.sort(key=lambda x: x[1], reverse=True)
    
    # Save to CSV file
    df = pd.DataFrame(results, columns=["Resume", "Similarity (%)", "Extracted Skills", "Matching Skills", "Missing Skills"])
    df.to_csv(output_file, index=False)
    print(f"✅ Ranking saved to {output_file} with resumes having similarity >= {threshold}%")

# Example usage
job_description_path = "preprocessed_text/job_descriptions/Business_Analyst.txt_text.txt"
resume_folder = "preprocessed_text/resumes"
output_csv = "ranked_resumes_with_skills.csv"

rank_resumes(job_description_path, resume_folder, output_csv, threshold=50.0)
