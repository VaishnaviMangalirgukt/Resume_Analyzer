import os

# Get list of processed files
processed_dir = "processed_text"
processed_files = set(os.listdir(processed_dir))

# Get list of labeled files (assuming labels correspond to processed file names without extension)
with open("labels.txt", "r") as f:
    labels = [line.strip() for line in f.readlines() if line.strip()]

# Assuming the labels file names match the processed files, find unnecessary files
valid_files = set([file.replace(".pdf_text.txt", "").strip() for file in labels])  # Adjust if needed

# Identify extra files
extra_files = [file for file in processed_files if file.replace(".pdf_text.txt", "").strip() not in valid_files]

# Delete extra files
for file in extra_files:
    file_path = os.path.join(processed_dir, file)
    os.remove(file_path)
    print(f"Deleted: {file_path}")

print("Cleanup completed!")
