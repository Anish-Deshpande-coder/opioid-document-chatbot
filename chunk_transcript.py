from docx import Document

def chunk_text(text, chunk_size=800, overlap=200):
    """
    Split text into overlapping chunks.
    
    chunk_size: target size of each chunk in characters
    overlap: how many characters to overlap between chunks
    """
    chunks = []
    start = 0
    
    while start < len(text):
        # Get a chunk
        end = start + chunk_size
        chunk = text[start:end]
        
        # Try to break at a sentence or paragraph if possible
        if end < len(text):
            # Look for last period in the chunk
            last_period = chunk.rfind('.')
            if last_period > chunk_size * 0.5:  # Only break if period is in second half
                end = start + last_period + 1
                chunk = text[start:end]
        
        chunks.append(chunk.strip())
        
        # Move start forward, accounting for overlap
        start = end - overlap
        
        # Avoid infinite loop at the end
        if start + chunk_size >= len(text) and end >= len(text):
            break
    
    return chunks

# Read the document
doc = Document("ID 1027 Transcript.docx")

# Extract all text
full_text = []
for paragraph in doc.paragraphs:
    if paragraph.text.strip():
        full_text.append(paragraph.text)

transcript = "\n\n".join(full_text)

# Chunk it
chunks = chunk_text(transcript, chunk_size=800, overlap=200)

# Display results
print(f"Original transcript: {len(transcript)} characters")
print(f"Number of chunks created: {len(chunks)}")
print("\n" + "="*60)
print("First 3 chunks:")
print("="*60)

for i, chunk in enumerate(chunks[:3]):
    print(f"\n--- Chunk {i+1} ({len(chunk)} chars) ---")
    print(chunk[:300] + "..." if len(chunk) > 300 else chunk)