import pickle
from sklearn.metrics.pairwise import cosine_similarity
from preprocessing import clean_text  # Assuming you already have this in 'preprocessing.py'

# Load pre-trained model and vectorizer
with open('job_matching_model.joblib', 'rb') as model_file:
    vectorizer, model = pickle.load(model_file)

# Function to get similarity score between a job description and resume
def get_similarity_score(resume, job_desc, vectorizer):
    # Preprocess the text
    preprocessed_resume = clean_text(resume)
    preprocessed_job_desc = clean_text(job_desc)

    # Vectorize the preprocessed text
    resume_vector = vectorizer.transform([preprocessed_resume])
    job_desc_vector = vectorizer.transform([preprocessed_job_desc])

    # Compute cosine similarity
    similarity = cosine_similarity(resume_vector, job_desc_vector)
    return similarity[0][0]

# Function to rank resumes based on similarity to the job description
def rank_resumes(job_desc, resumes, vectorizer):
    scores = []
    for resume in resumes:
        similarity_score = get_similarity_score(resume, job_desc, vectorizer)
        scores.append(similarity_score)

    # Rank the resumes based on similarity score
    ranked_resumes = sorted(zip(resumes, scores), key=lambda x: x[1], reverse=True)
    return ranked_resumes

# Example usage: Rank resumes based on a given job description
job_description = """
We are looking for a Full Stack Developer with experience in JavaScript, Node.js, React, and SQL.
The ideal candidate should have experience in both front-end and back-end technologies and be comfortable working in an Agile environment.
"""

resumes = [
    "Experienced software developer proficient in JavaScript, React, and Node.js.",
    "Full stack developer with experience in front-end and back-end technologies, including JavaScript and SQL.",
    "A data scientist with a passion for machine learning and deep learning algorithms.",
    "Senior software engineer with expertise in React, Node.js, and Agile practices."
]

# Rank the resumes
ranked_resumes = rank_resumes(job_description, resumes, vectorizer)

# Print the ranked resumes
print("Ranked Resumes:")
for i, (resume, score) in enumerate(ranked_resumes):
    print(f"Rank {i+1}: Similarity Score = {score:.4f}\nResume: {resume}\n")
