import os
import pandas as pd
import PyPDF2

# Folder paths
resume_folder = "preprocessed_text/resumes"
job_desc_folder = "preprocessed_text/job_descriptions"
output_csv = "preprocessed_text/dataset.csv"

# Ensure output folder exists
os.makedirs("preprocessed_text", exist_ok=True)

# Function to extract text from PDFs
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n" if page.extract_text() else ""
    return text.strip()

# Function to read text from .txt files
def read_txt_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read().strip()

# Collect data
data = []

# Process resumes
for filename in os.listdir(resume_folder):
    file_path = os.path.join(resume_folder, filename)
    if filename.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif filename.endswith(".txt"):
        text = read_txt_file(file_path)
    else:
        continue  # Skip unsupported file types

    data.append({"text": text, "label": "Resume"})

# Process job descriptions
for filename in os.listdir(job_desc_folder):
    file_path = os.path.join(job_desc_folder, filename)
    if filename.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif filename.endswith(".txt"):
        text = read_txt_file(file_path)
    else:
        continue  # Skip unsupported file types

    data.append({"text": text, "label": "Job Description"})

# Convert to DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv(output_csv, index=False)

print("✅ dataset.csv created successfully!")
