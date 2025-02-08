import sys
import os
from sentence_transformers import SentenceTransformer, util

# Check if the correct number of arguments are provided
if len(sys.argv) != 3:
    print("Usage: python match_resume_job.py <resume_text_file> <job_description_text_file>")
    sys.exit(1)

resume_path = sys.argv[1]
job_desc_path = sys.argv[2]

# Check if files exist
if not os.path.exists(resume_path):
    print(f"Error: File '{resume_path}' does not exist.")
    sys.exit(1)
if not os.path.exists(job_desc_path):
    print(f"Error: File '{job_desc_path}' does not exist.")
    sys.exit(1)

# Load text from files
def load_text(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

resume_text = load_text(resume_path)
job_desc_text = load_text(job_desc_path)

# Load the Sentence Transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Compute embeddings
resume_embedding = model.encode(resume_text, convert_to_tensor=True)
job_desc_embedding = model.encode(job_desc_text, convert_to_tensor=True)

# Compute cosine similarity
similarity_score = util.pytorch_cos_sim(resume_embedding, job_desc_embedding).item()

# Convert similarity score to percentage
similarity_percentage = similarity_score * 100

print(f"\n✅ Similarity Score: {similarity_percentage:.2f}%")
