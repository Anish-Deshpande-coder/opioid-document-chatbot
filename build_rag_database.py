from docx import Document
from portkey_ai import Portkey
import chromadb
import time

# Initialize Portkey
portkey = Portkey(
    base_url = "https://ai-gateway.apps.cloud.rt.nyu.edu/v1",
    api_key = "/JQz6HaQyeHdoEJQZivHGMiXqTQr",
    virtual_key = "vertexai"
)

def chunk_text(text, chunk_size=800, overlap=200):
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        
        if end < len(text):
            last_period = chunk.rfind('.')
            if last_period > chunk_size * 0.5:
                end = start + last_period + 1
                chunk = text[start:end]
        
        chunks.append(chunk.strip())
        start = end - overlap
        
        if start + chunk_size >= len(text) and end >= len(text):
            break
    
    return chunks

def create_embedding(text):
    """Create embedding for a text using Portkey."""
    response = portkey.embeddings.create(
        model = "gemini-embedding-001",
        input = text
    )
    return response.data[0].embedding

# Read the document
print("Reading document...")
doc = Document("ID 1027 Transcript.docx")
full_text = []
for paragraph in doc.paragraphs:
    if paragraph.text.strip():
        full_text.append(paragraph.text)
transcript = "\n\n".join(full_text)

# Chunk it
print("Chunking transcript...")
chunks = chunk_text(transcript, chunk_size=800, overlap=200)
print(f"Created {len(chunks)} chunks")

# Create ChromaDB collection
print("\nInitializing vector database...")
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.create_collection(name="veteran_transcript")

# Create embeddings and store in database
print("\nCreating embeddings for each chunk...")
for i, chunk in enumerate(chunks):
    print(f"Processing chunk {i+1}/{len(chunks)}...", end='\r')
    
    # Create embedding
    embedding = create_embedding(chunk)
    
    # Store in ChromaDB
    collection.add(
        embeddings=[embedding],
        documents=[chunk],
        ids=[f"chunk_{i}"]
    )
    
    # Small delay to avoid rate limits
    time.sleep(0.5)

print(f"\n\n✅ Success! Created RAG database with {len(chunks)} chunks")
print(f"Database collection: {collection.name}")
print(f"Total items: {collection.count()}")