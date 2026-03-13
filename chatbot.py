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

def display_results(results, question, n_results):
    """Display search results nicely."""
    print(f"\n{'='*80}")
    print(f"Question: {question}")
    print(f"{'='*80}\n")
    
    if len(results['documents'][0]) == 0:
        print("No results found.")
        return
    
    print(f"Top {len(results['documents'][0])} most relevant pages:\n")
    
    for i in range(len(results['documents'][0])):
        metadata = results['metadatas'][0][i]
        distance = results['distances'][0][i]
        similarity = 1 - distance
        
        print(f"--- Result {i+1} ---")
        print(f"📄 File: {metadata['filename']}")
        print(f"📃 Page: {metadata['page_number']}")
        print(f"Preview: {results['documents'][0][i][:250]}...")
        print()

print("="*80)
print("🤖 OPIOID DOCUMENT SEARCH CHATBOT")
print("="*80)
print("\nI can help you find relevant pages in the opioid documents!")
print("Database: 8,822 pages from 490 PDF files\n")
print("Commands:")
print("  - Type your question")
print("  - Start with a number to specify how many results (e.g., '10: your question')")
print("  - Type 'quit' or 'exit' to stop")
print("="*80)

while True:
    user_input = input("\n💬 Your question: ").strip()
    
    if user_input.lower() in ['quit', 'exit', 'q']:
        print("\n👋 Goodbye!")
        break
    
    if not user_input:
        continue
    
    # Check if user specified number of results
    n_results = 5  # default
    question = user_input
    
    if ':' in user_input:
        parts = user_input.split(':', 1)
        try:
            n_results = int(parts[0].strip())
            question = parts[1].strip()
        except:
            # If parsing fails, use the whole input as question
            pass
    
    # Limit to reasonable number
    n_results = min(max(n_results, 1), 20)
    
    print(f"\n🔍 Searching {n_results} most relevant pages...")
    
    try:
        results = search_documents(question, n_results=n_results)
        display_results(results, question, n_results)
    except Exception as e:
        print(f"\n❌ Error: {e}")