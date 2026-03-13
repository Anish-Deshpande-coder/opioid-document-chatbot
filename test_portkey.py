from portkey_ai import Portkey

portkey = Portkey(
    base_url = "https://ai-gateway.apps.cloud.rt.nyu.edu/v1",
    api_key = "/JQz6HaQyeHdoEJQZivHGMiXqTQr",
    virtual_key = "vertexai"
)

# Test the embedding model
embedding = portkey.embeddings.create(
    model = "gemini-embedding-001",
    input = "Hello, this is a test!"
)

print("Success! Embedding created:")
print(embedding)