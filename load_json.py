import json

# Step 1: Open and load the JSON file
with open('labels.json', 'r') as file:
    labels = json.load(file)  # This will convert JSON to a Python dictionary

# Step 2: Access or print the loaded data
print(labels)  # Print the entire content of the JSON file

# Step 3: You can also access specific data like this:
for resume, job_description in labels.items():
    print(f"Resume: {resume} --> Job Description: {job_description}")
