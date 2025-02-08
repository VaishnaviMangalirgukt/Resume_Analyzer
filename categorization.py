import json
import os

# Load the labels.json file
with open('labels.json', 'r') as f:
    labels_data = json.load(f)

# Create a dictionary from the job titles to labels for faster lookup
job_title_to_label = {job['job_title']: job['label'] for job in labels_data}

# Function to categorize resumes or job descriptions
def categorize(text):
    # For this example, we're looking for job titles in the text and categorizing them.
    for job_title in job_title_to_label:
        if job_title.lower() in text.lower():
            return job_title_to_label[job_title]  # Return the corresponding label
    return "Uncategorized"  # Return this if no job title match is found

# Process resumes in the folder
def process_resumes_and_jobs(resume_dir, job_desc_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Process resumes
    for filename in os.listdir(resume_dir):
        file_path = os.path.join(resume_dir, filename)
        output_path = os.path.join(output_dir, filename + "_category.txt")

        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # Categorize the resume
        category = categorize(text)

        # Save the categorized result
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(f"Job Category: {category}\n\n")
            output_file.write(f"Extracted Text: \n{text}")

        print(f"Processed resume {filename} and saved category to {output_path}")

    # Process job descriptions
    for filename in os.listdir(job_desc_dir):
        file_path = os.path.join(job_desc_dir, filename)
        output_path = os.path.join(output_dir, filename + "_category.txt")

        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # Categorize the job description
        category = categorize(text)

        # Save the categorized result
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(f"Job Category: {category}\n\n")
            output_file.write(f"Extracted Text: \n{text}")

        print(f"Processed job description {filename} and saved category to {output_path}")

# Example usage
if __name__ == "__main__":
    resume_dir = 'extracted_text/resumes'  # Folder containing resumes
    job_desc_dir = 'extracted_text/job_descriptions'  # Folder containing job descriptions
    output_dir = 'categorized_output'  # Folder to save categorized results
    process_resumes_and_jobs(resume_dir, job_desc_dir, output_dir)
