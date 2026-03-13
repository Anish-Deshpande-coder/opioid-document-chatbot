from docx import Document

# Read the Word document
doc = Document("ID 1027 Transcript.docx")

# Extract all text
full_text = []
for paragraph in doc.paragraphs:
    if paragraph.text.strip():  # Only add non-empty paragraphs
        full_text.append(paragraph.text)

# Join all paragraphs with newlines
transcript = "\n\n".join(full_text)

# Print the first 500 characters to see if it worked
print("First 500 characters of the transcript:")
print(transcript[:500])
print("\n...")
print(f"\nTotal length: {len(transcript)} characters")