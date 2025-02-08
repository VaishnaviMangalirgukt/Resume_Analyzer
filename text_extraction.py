import os
import PyPDF2
from docx import Document

# Function to read text from a PDF file
def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

# Function to read text from a DOCX file
def extract_text_from_docx(docx_path):
    try:
        doc = Document(docx_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
        return ""

# Function to read text from a TXT file (for job descriptions)
def extract_text_from_txt(txt_path):
    try:
        with open(txt_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading text from TXT: {e}")
        return ""

# Function to process files in a directory
def process_files(input_dir, output_dir, file_type):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename + "_text.txt")

        if filename.lower().endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        elif filename.lower().endswith('.docx'):
            text = extract_text_from_docx(file_path)
        elif filename.lower().endswith('.txt'):
            text = extract_text_from_txt(file_path)
        else:
            print(f"Skipping non-supported {file_type} file: {filename}")
            continue

        # Save extracted text to a file
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(text)
        print(f"Processed {file_type} {filename} and saved to {output_path}")

# Main function
if __name__ == "__main__":
    resume_dir = 'resumes'  # Folder containing resumes (PDF/DOCX)
    job_desc_dir = 'job_descriptions'  # Folder containing job descriptions (TXT)
    output_resumes_dir = 'extracted_text/resumes'  
    output_job_desc_dir = 'extracted_text/job_descriptions'

    process_files(resume_dir, output_resumes_dir, "resume")
    process_files(job_desc_dir, output_job_desc_dir, "job description")
