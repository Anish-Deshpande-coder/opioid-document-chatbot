from portkey_ai import Portkey
import chromadb

# Initialize Portkey
portkey = Portkey(
    base_url = "https://ai-gateway.apps.cloud.rt.nyu.edu/v1",
    api_key = "/JQz6HaQyeHdoEJQZivHGMiXqTQr",
    virtual_key = "vertexai"
)

def create_embedding(text):
    """Create embedding for a text."""
    response = portkey.embeddings.create(
        model = "gemini-embedding-001",
        input = text
    )
    return response.data[0].embedding

def search_transcript(question, n_results=3):
    """Search the transcript for relevant chunks."""
    # Connect to database
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection(name="veteran_transcript")
    
    # Create embedding for the question
    question_embedding = create_embedding(question)
    
    # Search for similar chunks
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=n_results
    )
    
    return results

# Test it!
question = "Did the veteran mention anything about rights to opioids?"

print(f"Question: {question}\n")
print("="*60)
print("Searching transcript...\n")

results = search_transcript(question, n_results=3)

print(f"Found {len(results['documents'][0])} relevant chunks:\n")

for i, chunk in enumerate(results['documents'][0]):
    print(f"--- Result {i+1} ---")
    print(chunk[:400] + "..." if len(chunk) > 400 else chunk)
    print()