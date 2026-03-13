from flask import Flask, request, jsonify
from flask_cors import CORS
from portkey_ai import Portkey
import chromadb
import os

app = Flask(__name__)
CORS(app)

# Initialize Portkey
portkey = Portkey(
    base_url="https://ai-gateway.apps.cloud.rt.nyu.edu/v1",
    api_key=os.environ.get("PORTKEY_API_KEY"),
    virtual_key="vertexai"
)

def create_embedding(text):
    response = portkey.embeddings.create(
        model="gemini-embedding-001",
        input=text
    )
    return response.data[0].embedding

def search_documents(question, n_results=5):
    client = chromadb.PersistentClient(path="./chroma_db_pdfs")
    collection = client.get_collection(name="opioid_documents")
    question_embedding = create_embedding(question)
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=n_results,
        include=['documents', 'metadatas', 'distances']
    )
    return results

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    question = data.get('question', '')
    n_results = data.get('n_results', 5)

    if not question:
        return jsonify({'error': 'No question provided'}), 400

    try:
        results = search_documents(question, n_results)
        formatted_results = []
        for i in range(len(results['documents'][0])):
            metadata = results['metadatas'][0][i]
            distance = results['distances'][0][i]
            similarity = 1 - distance
            formatted_results.append({
                'rank': i + 1,
                'filename': metadata['filename'],
                'page_number': metadata['page_number'],
                'relevance_score': float(similarity),
                'preview': results['documents'][0][i][:300]
            })
        return jsonify({'question': question, 'results': formatted_results})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
