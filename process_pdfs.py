import zipfile
import os

# Extract the zip file
zip_path = "C:/Users/anish/Downloads/2ndAmend_5.zip"
extract_to = "./2ndAmend_5"

print("Extracting zip file...")
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_to)

print(f"Extracted to {extract_to}")

# Count PDF files
pdf_count = 0
for root, dirs, files in os.walk(extract_to):
    for file in files:
        if file.endswith('.pdf'):
            pdf_count += 1

print(f"Found {pdf_count} PDF files")