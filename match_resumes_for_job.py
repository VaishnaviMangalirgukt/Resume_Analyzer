import sys
import os
from sentence_transformers import SentenceTransformer, util

# Load the pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')

def load_text(file_path):
    """Load text from a given file path."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"❌ Error: File '{file_path}' does not exist.")
        sys.exit(1)

def rank_resumes(job_description_file, resumes_folder='preprocessed_text/resumes'):
    """Rank multiple resumes based on similarity with a job description."""
    
    # Load job description text
    job_text = load_text(job_description_file)
    
    # Load all resumes from the folder
    resume_files = [f for f in os.listdir(resumes_folder) if f.endswith('.txt')]
    
    if not resume_files:
        print("❌ No resumes found in the folder.")
        return
    
    resume_texts = {file: load_text(os.path.join(resumes_folder, file)) for file in resume_files}
    
    # Encode job description and resumes
    job_embedding = model.encode(job_text, convert_to_tensor=True)
    resume_embeddings = {file: model.encode(text, convert_to_tensor=True) for file, text in resume_texts.items()}
    
    # Compute similarity scores
    similarity_scores = {file: util.pytorch_cos_sim(job_embedding, embedding).item() * 100 for file, embedding in resume_embeddings.items()}
    
    # Sort resumes by similarity score (highest first)
    ranked_resumes = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)
    
    print("\n✅ Ranked Resumes for Job Description:\n")
    for rank, (file, score) in enumerate(ranked_resumes, start=1):
        print(f"{rank}. {file} - Similarity: {score:.2f}%")
    
    return ranked_resumes

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python rank_resumes_job.py <job_description_text_file>")
        sys.exit(1)
    
    job_description_file = sys.argv[1]
    rank_resumes(job_description_file)
