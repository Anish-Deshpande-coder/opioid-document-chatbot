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

def search_documents(question, n_results=5):
    """Search for relevant pages."""
    # Connect to database
    client = chromadb.PersistentClient(path="./chroma_db_pdfs")
    collection = client.get_collection(name="opioid_documents")
    
    # Create embedding for the question
    question_embedding = create_embedding(question)
    
    # Search for similar pages
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=n_results,
        include=['documents', 'metadatas', 'distances']
    )
    
    return results

# Test it!
question = "Are there narratives that brands pitched opioids as a right?"

print(f"Question: {question}\n")
print("="*80)
print("Searching documents...\n")

results = search_documents(question, n_results=5)

print(f"Found top {len(results['documents'][0])} most relevant pages:\n")

for i in range(len(results['documents'][0])):
    metadata = results['metadatas'][0][i]
    distance = results['distances'][0][i]
    # Convert distance to similarity score (0-1, where 1 is most similar)
    similarity = 1 - distance
    
    print(f"--- Result {i+1} ---")
    print(f"File: {metadata['filename']}")
    print(f"Page: {metadata['page_number']}")
    print(f"Relevance Score: {similarity:.4f}")
    print(f"Preview: {results['documents'][0][i][:300]}...")
    print()