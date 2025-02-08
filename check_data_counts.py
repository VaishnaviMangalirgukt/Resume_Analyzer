import os

print("Processed resumes:", len(os.listdir("processed_text")))
print("Labels count:", len(open("labels.txt").readlines()))
