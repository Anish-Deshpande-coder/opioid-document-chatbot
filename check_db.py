import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

# List all collections
collections = client.list_collections()

print("Collections in database:")
for col in collections:
    print(f"  - {col.name} (count: {col.count()})")