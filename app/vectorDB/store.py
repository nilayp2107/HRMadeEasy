''' This file contains procedure which can encode a pdf file to 
        vector Embeddings and then store to json document.
    Functions:
    1. chunk_text(text, chunk_size=20) - Function to chunk text
    2. embed_chunks(chunks) - Function to generate embeddings of the chunks
    3. build_faiss_index(embeddings) - Store indexes in Memory
    4. store_faiss_index(index) - Store Indexes to Disk
'''

# import libraries
import faiss
import fitz
from sentence_transformers import SentenceTransformer
import json
import numpy as np

# Mode for generating Embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# load_pdf(path) - Function to Load PDF to Text (Utility)
# input: 
#   path(string) - Path to the pdf File
# output: 
#   Text from PDF file
# Notes
#
def load_pdf(path):
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text("text")
    return text


# chunk_text(text) - Function to chunk text
# input: 
#   text(string) - text to be chunked
#   chunk_size(int) - number of words in each chunk
# output: 
#   list of words in chunk 
# Notes
#
def chunk_text(text, chunk_size=20):
    # Split the text into words (tokenization)
    words = text.split() 
    # Move through each words with a step of chunk_size
    for i in range(0, len(words), chunk_size):
        # return the chunk 
        yield " ".join(words[i:i+chunk_size]) 


# embed_chunks(chunks) - Function to generate embeddings of the chunks
# input: 
#   chunks(list) - list of chunks to be encoded
# output: 
#   list of embeddings 
# Notes
#
def embed_chunks(chunks):
    embeddings = []
    for chunk in chunks:
        embeddings.append(model.encode(chunk))
        print(model.encode(chunk))
    return embeddings

# build_faiss_index(embeddings) - Store the embeddings in a RAM
# input: 
#   embeddings(np.ndarray) - array of (array of embeddings in float)
# output: 
#   list of normalised embeddings 
# Notes:
#   what does faiss.IndexFlatL2(dim) do? along with index.add()
def build_faiss_index(embeddings: np.ndarray):
    # Ensure embeddings are in float32 (FAISS requirement)
    if embeddings.dtype != np.float32:
        embeddings = embeddings.astype(np.float32)
    
    dimension = embeddings.shape[1]  # embedding dimension
    index = faiss.IndexFlatL2(dimension)  # L2 distance (cosine similarity needs normalization)
    
    index.add(embeddings)  # Add all embeddings to the index
    return index

# store_faiss_index(index) - Store the embeddings in a disk
# input: 
#   index - array of (array of embeddings in float)
# output: 
#   None 
# Notes:
#   what does faiss.IndexFlatL2(dim) do? along with index.add()
def store_faiss_index(index):
    faiss.write_index(index, "vectorDB.faiss")

def store_embeddings(pdf_paths):
    docs = []
    all_embeddings = []

    # for each pdf do this
    for pdf_id, path in enumerate(pdf_paths):
        # Convert the each pdf to text
        text = load_pdf(path) 
        # Chunking
        chunks = list(chunk_text(text)) 
        # Embeddings generation
        embeddings = model.encode(chunks)
        # Aggregate of embeddings
        all_embeddings.append(embeddings)
        # Metadata Storage
        for i, chunk in enumerate(chunks):
            docs.append({
                "pdf_id": pdf_id,
                "chunk_id": i,
                "text": chunk,
                "source": path
            })
    # Type cast for faiss compatibilty     
    all_embeddings = np.vstack(all_embeddings)
    # Generate Indexes
    index = build_faiss_index(all_embeddings)
    # store indexes
    store_faiss_index(index)
    # Store the metadata
    with open("docs.json", "w") as f:
        json.dump(docs, f)


# main calls

pdf_paths = ["documents/v11_leave.pdf", "documents/v11_policies.pdf", "documents/v11_benefits.pdf"]
store_embeddings(pdf_paths)
