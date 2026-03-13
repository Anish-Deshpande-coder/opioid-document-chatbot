import os
import PyPDF2
from portkey_ai import Portkey
import chromadb
import time

# Initialize Portkey
portkey = Portkey(
    base_url = "https://ai-gateway.apps.cloud.rt.nyu.edu/v1",
    api_key = "/JQz6HaQyeHdoEJQZivHGMiXqTQr",
    virtual_key = "vertexai"
)

def create_embedding(text):
    """Create embedding for text using Portkey."""
    response = portkey.embeddings.create(
        model = "gemini-embedding-001",
        input = text
    )
    return response.data[0].embedding

def process_pdf(pdf_path, filename):
    """Extract text from each page of a PDF."""
    pages = []
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                
                # Only keep pages with substantial text
                if text and len(text.strip()) > 100:
                    pages.append({
                        'filename': filename,
                        'page_number': page_num + 1,
                        'text': text.strip()
                    })
    except Exception as e:
        print(f"Error processing {filename}: {e}")
    
    return pages

# Create database
print("Initializing database...")
client = chromadb.PersistentClient(path="./chroma_db_pdfs")
# Create new collection (or get existing one)
try:
    collection = client.create_collection(name="opioid_documents")
except:
    # Collection already exists, delete and recreate
    client.delete_collection(name="opioid_documents")
    collection = client.create_collection(name="opioid_documents")

# Process all PDFs
pdf_folder = "./2ndAmend_5/2ndAmend_5"
all_pages = []
pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]

print(f"Found {len(pdf_files)} PDF files")
print("Processing PDFs...")

for idx, filename in enumerate(pdf_files):
    pdf_path = os.path.join(pdf_folder, filename)
    print(f"Processing {idx+1}/{len(pdf_files)}: {filename}...", end='\r')
    
    pages = process_pdf(pdf_path, filename)
    all_pages.extend(pages)

print(f"\nExtracted {len(all_pages)} pages with text")

# Create embeddings and store
print("\nCreating embeddings and storing in database...")
for idx, page_data in enumerate(all_pages):
    print(f"Processing page {idx+1}/{len(all_pages)}...", end='\r')
    
    # Create embedding
    embedding = create_embedding(page_data['text'])
    
    # Store in database with metadata
    collection.add(
        embeddings=[embedding],
        documents=[page_data['text']],
        metadatas=[{
            'filename': page_data['filename'],
            'page_number': page_data['page_number']
        }],
        ids=[f"{page_data['filename']}_page_{page_data['page_number']}"]
    )
    
    # Small delay to avoid rate limits
    time.sleep(0.5)

print(f"\n\n✅ Success! Processed {len(all_pages)} pages")
print(f"Database collection: {collection.name}")
print(f"Total items: {collection.count()}")