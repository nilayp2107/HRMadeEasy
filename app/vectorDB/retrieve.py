''' This file contains procedure which can help us to retrieve the embeddings and the text along with the queries.
    Functions:
    1. 
'''
import faiss
from sentence_transformers import SentenceTransformer
import json
import os

BASE_DIR = os.path.dirname(__file__)
# Model which we are using
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load the vector DB
index = faiss.read_index(os.path.join(BASE_DIR, "vectorDB.faiss"))
with open(os.path.join(BASE_DIR, "docs.json"), "r") as f:
    docs = json.load(f)

# Function called by the app.py
def similarity_search(query):
    query_embedding = model.encode([query])
    D, I = index.search(query_embedding, k=3)  # top 3 matches
    # Store the result in it
    results = []
    for idx in I[0]:
        chunk_info = docs[idx]   # docs list is aligned with embeddings
        results.append({
            "chunk_id": chunk_info["chunk_id"],
            "pdf_id": chunk_info["pdf_id"],
            "source": chunk_info["source"],
            "text": chunk_info["text"],
            "distance": float(D[0][list(I[0]).index(idx)])  # optional: attach distance
        })
    text = ""
    for res in results:
        text += res["text"]
    return text

# # Now you can search:
# query = "Leave per year"
# query_embedding = model.encode([query])
# print(similarity_search(query))
# results = similarity_search(query)


# for res in results:
#     print(f"\nPDF: {res['source']} | Chunk ID: {res['chunk_id']}")
#     print(f"Distance: {res['distance']:.4f}")
#     print(res["text"])
