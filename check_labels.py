import os

# Get the list of processed resumes and labels
processed_resumes = os.listdir("processed_text")
with open("labels.txt", "r") as file:
    labels = file.readlines()

# Check the counts of processed resumes and labels
print("Processed resumes:", len(processed_resumes))
print("Labels count:", len(labels))

# Verify that the filenames and labels match
for resume, label in zip(processed_resumes, labels):
    print(f"Resume: {resume}, Label: {label.strip()}")
