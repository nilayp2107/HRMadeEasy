
from flask import Flask, render_template, request, jsonify
from sentence_transformers import SentenceTransformer
import numpy as np


app = Flask(__name__)

# Load the embedding model once at startup
model = SentenceTransformer('all-MiniLM-L6-v2')

@app.route('/')
def index():
    return render_template('chat.html')


@app.route('/send', methods=['POST'])
def send():
    data = request.get_json()
    prompt = data.get('prompt', '')
    print(f"User prompt: {prompt}")
    # Encode the prompt to get the embedding
    embedding = model.encode(prompt)
    # Print only the first float of the embedding
    print("First float of embedding:", float(embedding[0]))
    # Optionally, return the value in the response for testing
    return jsonify({'response': f'First float of embedding: {float(embedding[0])}'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
